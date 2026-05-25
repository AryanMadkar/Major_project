from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
import re
from extractor.GraphState import GraphState
from extractor.bhk import extract_bhk
from extractor.Response import response_node
from extractor.Type import extract_type
from extractor.cleaned import clean_text_node

builder = StateGraph(GraphState)
builder.add_node("clean_text", clean_text_node)
builder.add_node("extract_request_type", extract_type)
builder.add_node("extract_bhk", extract_bhk)
builder.add_node("response", response_node)

builder.set_entry_point("clean_text")

builder.add_edge("clean_text", "extract_request_type")
builder.add_edge("clean_text", "extract_bhk")
builder.add_edge(["extract_request_type", "extract_bhk"], "response")
builder.add_edge("response", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({
        "user_input": "I am looking for a 2 BHK apartment."
    })
    print("Final Graph State:", result)