from langgraph.graph import StateGraph, END
from extractor.GraphState import GraphState
from extractor.bhk import extract_bhk
from extractor.Response import response_node
from extractor.Type import extract_type
from extractor.cleaned import clean_text_node
from extractor.price_extractor import extract_price


builder = StateGraph(GraphState)
builder.add_node("clean_text", clean_text_node)
builder.add_node("extract_request_type", extract_type)
builder.add_node("extract_bhk", extract_bhk)
builder.add_node("response", response_node)
builder.add_node("extract_price", extract_price)

builder.set_entry_point("clean_text")

builder.add_edge("clean_text", "extract_request_type")
builder.add_edge("clean_text", "extract_bhk")
builder.add_edge("extract_request_type", "extract_price")
builder.add_edge(["extract_request_type", "extract_bhk", "extract_price"], "response")
builder.add_edge("response", END)

graph = builder.compile()

if __name__ == "__main__":
    png_data = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_data)

    result = graph.invoke({
        "user_input": """1 BHK
            Kanakya park
            With car parking
            Asking 1.05 lakhs and deposit 2 lakhs"""
    })
    final_state = {key: value for key, value in result.items() if value is not None}
    print("Final Graph State:", final_state)