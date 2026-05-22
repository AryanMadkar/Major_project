# =====================================================
# main.py — FastAPI application entry point
#
# Exposes two routes:
#   GET  /          → a browser UI for manual testing
#   POST /verify    → the speaker verification API
# =====================================================

import os
import shutil
import sys
import uuid
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse


# ── Import resolution ────────────────────────────────
# Supports two launch modes:
#   1. `uvicorn app.main:app` (package mode, __package__ is set)
#   2. `python main.py`       (script mode, __package__ is None)

if __package__:
    from .graph import graph
    from .utils.audio import optimize_audio_file
    from .schemas import VerificationResponse
else:
    # When run as a plain script, add the project root to sys.path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.graph import graph
    from app.utils.audio import optimize_audio_file
    from app.schemas import VerificationResponse


# ── FastAPI app ──────────────────────────────────────
app = FastAPI(
    title="Speaker Verification API",
    description="Multi-model speaker verification using ECAPA-TDNN and TitaNet-Large",
    version="1.0.0"
)


# ── Upload directories ───────────────────────────────
# Raw uploads land in UPLOAD_DIR.
# Preprocessed (VAD + resampled) files go in OPTIMIZED_DIR.
UPLOAD_DIR    = "uploads"
OPTIMIZED_DIR = os.path.join(UPLOAD_DIR, "optimized")

os.makedirs(UPLOAD_DIR,    exist_ok=True)
os.makedirs(OPTIMIZED_DIR, exist_ok=True)


# ── Helper ───────────────────────────────────────────

def save_upload(upload: UploadFile, dest_dir: str) -> str:
    """
    Save an uploaded file to *dest_dir* with a unique name
    so concurrent requests never overwrite each other.

    Returns the absolute path of the saved file.
    """

    # Preserve the original extension; default to .wav
    original_name = upload.filename or "audio.wav"
    extension     = os.path.splitext(original_name)[-1].lower() or ".wav"

    # Unique filename prevents race conditions under load
    unique_name = f"{uuid.uuid4().hex}{extension}"
    dest_path   = os.path.join(dest_dir, unique_name)

    with open(dest_path, "wb") as f:
        shutil.copyfileobj(upload.file, f)

    return dest_path


# ── Routes ───────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    """
    Serve a simple browser UI so you can test the API
    without needing curl or Postman.
    """
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Speaker Verification</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f0f13;
      color: #e8e8f0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .card {
      background: #1a1a24;
      border: 1px solid #2a2a3a;
      border-radius: 16px;
      padding: 2.5rem;
      max-width: 520px;
      width: 100%;
      box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    }
    h1 {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      background: linear-gradient(90deg, #7c8cf8, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    p.sub { color: #888; font-size: 0.875rem; margin-bottom: 2rem; }
    .field { margin-bottom: 1.2rem; }
    label { display: block; font-size: 0.8rem; color: #aaa; margin-bottom: 0.4rem; letter-spacing: 0.05em; text-transform: uppercase; }
    input[type=file] {
      width: 100%;
      padding: 0.6rem 0.8rem;
      background: #0f0f18;
      border: 1px solid #2e2e42;
      border-radius: 8px;
      color: #e8e8f0;
      font-size: 0.9rem;
      cursor: pointer;
    }
    button {
      width: 100%;
      padding: 0.85rem;
      background: linear-gradient(135deg, #5b5ef4, #7c3aed);
      color: #fff;
      border: none;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 0.5rem;
      transition: opacity 0.2s;
    }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    #result {
      margin-top: 1.8rem;
      padding: 1.2rem;
      background: #12121c;
      border-radius: 10px;
      border: 1px solid #2a2a3a;
      display: none;
    }
    .verdict {
      font-size: 1.3rem;
      font-weight: 700;
      margin-bottom: 0.8rem;
    }
    .same  { color: #4ade80; }
    .diff  { color: #f87171; }
    .meta  { font-size: 0.82rem; color: #888; margin-bottom: 1rem; }
    .votes { border-top: 1px solid #2a2a3a; padding-top: 0.8rem; }
    .vote-row {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      padding: 0.3rem 0;
      border-bottom: 1px solid #1e1e2c;
    }
    .vote-row:last-child { border-bottom: none; }
    .badge {
      padding: 0.15rem 0.55rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .badge.yes { background: #14532d; color: #4ade80; }
    .badge.no  { background: #450a0a; color: #f87171; }
    #status { color: #a78bfa; font-size: 0.85rem; margin-top: 0.8rem; min-height: 1.2em; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🎙 Speaker Verification</h1>
    <p class="sub">Upload two WAV recordings to check if they belong to the same person.</p>

    <div class="field">
      <label>Audio File 1</label>
      <input type="file" id="f1" accept=".wav" />
    </div>
    <div class="field">
      <label>Audio File 2</label>
      <input type="file" id="f2" accept=".wav" />
    </div>

    <button id="btn" onclick="run()">Verify Speaker</button>
    <div id="status"></div>

    <div id="result">
      <div class="verdict" id="verdict"></div>
      <div class="meta" id="meta"></div>
      <div class="votes" id="votes"></div>
    </div>
  </div>

  <script>
    async function run() {
      const f1 = document.getElementById('f1').files[0];
      const f2 = document.getElementById('f2').files[0];
      const btn = document.getElementById('btn');
      const status = document.getElementById('status');

      if (!f1 || !f2) { alert('Please select both audio files.'); return; }

      btn.disabled = true;
      status.textContent = 'Processing… this may take 10–30 seconds.';
      document.getElementById('result').style.display = 'none';

      const fd = new FormData();
      fd.append('audio1', f1);
      fd.append('audio2', f2);

      try {
        const resp = await fetch('/verify', { method: 'POST', body: fd });
        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.detail || resp.statusText);
        }
        const data = await resp.json();
        showResult(data);
      } catch (e) {
        status.textContent = 'Error: ' + e.message;
      } finally {
        btn.disabled = false;
      }
    }

    function showResult(data) {
      document.getElementById('status').textContent = '';
      const same = data.final_decision;
      document.getElementById('verdict').innerHTML =
        same
          ? '<span class="same">✅ Same Speaker</span>'
          : '<span class="diff">❌ Different Speaker</span>';
      document.getElementById('meta').textContent =
        `Confidence: ${(data.confidence * 100).toFixed(1)}%  |  Votes: ${data.votes.filter(v=>v.same_speaker).length} / ${data.votes.length}`;

      const votesEl = document.getElementById('votes');
      votesEl.innerHTML = data.votes.map(v => `
        <div class="vote-row">
          <span>${v.model.toUpperCase()}  <small style="color:#555">score: ${v.score}</small></span>
          <span class="badge ${v.same_speaker ? 'yes' : 'no'}">${v.same_speaker ? 'Same' : 'Different'}</span>
        </div>
      `).join('');

      document.getElementById('result').style.display = 'block';
    }
  </script>
</body>
</html>
""")


@app.post("/verify", response_model=VerificationResponse)
async def verify_speaker(
    audio1: UploadFile = File(..., description="First  speaker WAV file"),
    audio2: UploadFile = File(..., description="Second speaker WAV file"),
):
    """
    Compare two audio recordings and return whether they
    belong to the same speaker.

    Workflow:
        1. Save uploaded files with unique names
        2. Preprocess: resample → mono → normalise → VAD
        3. Run ECAPA, TitaNet, and Optimised in parallel
        4. Return majority-vote decision + per-model scores
    """

    # Paths we'll need to clean up in the finally block
    raw_paths       = []
    optimised_paths = []

    try:
        # ── Step 1: Persist uploaded files ──────────────
        path1 = save_upload(audio1, UPLOAD_DIR)
        path2 = save_upload(audio2, UPLOAD_DIR)
        raw_paths = [path1, path2]

        # ── Step 2: Preprocess (VAD, resample, normalise) ─
        opt_path1 = optimize_audio_file(path1, OPTIMIZED_DIR)
        opt_path2 = optimize_audio_file(path2, OPTIMIZED_DIR)
        optimised_paths = [opt_path1, opt_path2]

        # ── Step 3: Run the LangGraph pipeline ──────────
        # graph.invoke() runs parallel_models → voting and
        # returns the full GraphState dict.
        state = graph.invoke({
            "audio1": opt_path1,
            "audio2": opt_path2,
        })

        # ── Step 4: Return the voting node's output ──────
        return state["final_result"]

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        # Bad audio format, no speech detected, etc.
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        # Catch-all: log the full traceback server-side,
        # return a sanitised message to the client.
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}"
        )

    finally:
        # ── Cleanup: delete temp files regardless of outcome ─
        # This prevents the uploads/ folder from growing
        # unboundedly in production.
        for p in raw_paths + optimised_paths:
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass   # non-fatal; log if you have a logger set up


# ── Local dev entry point ────────────────────────────

if __name__ == "__main__":
    import uvicorn
    # Run with auto-reload during development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True     # watches for file changes
    )