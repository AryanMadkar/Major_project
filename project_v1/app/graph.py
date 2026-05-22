# =====================================================
# graph.py — LangGraph orchestration
#
# This module wires the three agents together using
# LangGraph's StateGraph. The execution flow is:
#
#   [START]
#      │
#      ▼
#   parallel_models   ← runs all 3 agents simultaneously
#      │                 using a thread pool
#      ▼
#   voting            ← majority vote (≥2/3) + avg score
#      │
#      ▼
#   [END]
# =====================================================

from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor

from langgraph.graph import StateGraph, END


# ── Agent imports with graceful fallback ─────────────
# If a model's heavy dependency (e.g. NeMo, SpeechBrain)
# is missing, the agent is replaced with a stub that
# returns a failure dict so the rest of the pipeline
# still runs and returns a partial result.

try:
    from .agents.ecapa_agent import verify as ecapa_verify
except Exception as e:
    print(f"[graph] WARNING: ECAPA agent unavailable — {e}")
    error_msg = str(e)
    def ecapa_verify(a, b):
        return {"model": "ecapa",    "score": 0.0, "same_speaker": False, "error": error_msg}

try:
    from .agents.titanet_agent import verify as titanet_verify
except Exception as e:
    print(f"[graph] WARNING: TitaNet agent unavailable — {e}")
    error_msg = str(e)
    def titanet_verify(a, b):
        return {"model": "titanet",  "score": 0.0, "same_speaker": False, "error": error_msg}

try:
    from .agents.optimized_agent import verify as optimized_verify
except Exception as e:
    print(f"[graph] WARNING: Optimized agent unavailable — {e}")
    error_msg = str(e)
    def optimized_verify(a, b):
        return {"model": "optimized","score": 0.0, "same_speaker": False, "error": error_msg}


# ── State schema ─────────────────────────────────────
# LangGraph passes this dict between nodes.
# TypedDict gives us type hints without runtime overhead.

class GraphState(TypedDict):
    audio1:           str    # path to first  optimised WAV file
    audio2:           str    # path to second optimised WAV file
    ecapa_result:     dict   # output of ecapa_agent.verify()
    titanet_result:   dict   # output of titanet_agent.verify()
    optimized_result: dict   # output of optimized_agent.verify()
    final_result:     dict   # output of the voting node


# ── Node 1 — Parallel model execution ───────────────

def run_parallel_models(state: GraphState) -> dict:
    """
    Submit all three agent.verify() calls to a
    ThreadPoolExecutor so they run concurrently.

    On a GPU machine each agent runs sequentially on
    the GPU, so parallelism mostly helps the CPU-bound
    parts (audio loading, numpy ops).  On CPU it gives
    true parallelism across cores.
    """

    audio1 = state["audio1"]
    audio2 = state["audio2"]

    # ThreadPoolExecutor starts the threads and we
    # collect results via .result() which blocks until
    # each future is complete.
    with ThreadPoolExecutor(max_workers=3) as executor:

        # Submit all three tasks at the same time
        future_ecapa    = executor.submit(ecapa_verify,    audio1, audio2)
        future_titanet  = executor.submit(titanet_verify,  audio1, audio2)
        future_optimized= executor.submit(optimized_verify,audio1, audio2)

        # .result() waits for the thread to finish and
        # re-raises any exception that occurred inside it
        ecapa_result    = future_ecapa.result()
        titanet_result  = future_titanet.result()
        optimized_result= future_optimized.result()

    # Returning a dict from a node causes LangGraph to
    # merge these keys into the shared GraphState.
    return {
        "ecapa_result":     ecapa_result,
        "titanet_result":   titanet_result,
        "optimized_result": optimized_result,
    }


# ── Node 2 — Majority vote ───────────────────────────

def voting_node(state: GraphState) -> dict:
    """
    Combine the three model decisions using majority vote.

    Decision: same_speaker = True  if at least 2 of 3
              models agree.
    Confidence: average cosine similarity across models.
    """

    results = [
        state["ecapa_result"],
        state["titanet_result"],
        state["optimized_result"],
    ]

    # Count how many models voted "same speaker"
    votes = sum(r["same_speaker"] for r in results)

    # Majority vote: need at least 2 out of 3
    final_decision = votes >= 2

    # Average similarity score as a proxy for confidence
    confidence = sum(r["score"] for r in results) / len(results)

    return {
        "final_result": {
            "final_decision": final_decision,       # bool
            "confidence":     round(confidence, 4), # float
            "votes":          results,              # per-model breakdown
        }
    }


# ── Build & compile the graph ────────────────────────

builder = StateGraph(GraphState)

# Register nodes (name → function)
builder.add_node("parallel_models", run_parallel_models)
builder.add_node("voting",          voting_node)

# Set entry point
builder.set_entry_point("parallel_models")

# Define edges (execution order)
builder.add_edge("parallel_models", "voting")
builder.add_edge("voting",          END)

# compile() validates the graph and returns a runnable
graph = builder.compile()