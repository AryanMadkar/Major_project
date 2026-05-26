from langgraph.graph import StateGraph, END
import json
from extractor.GraphState import GraphState
from extractor.bhk import extract_bhk
from extractor.Response import response_node
from extractor.Type import extract_type
from extractor.cleaned import clean_text_node
from extractor.price_extractor import extract_price
from extractor.location_extractor import extract_location
from extractor.furnishing_extractor import extract_furnishing
from extractor.facing_extractor import extract_facing
from extractor.amenities_extractor import extract_amenities
from extractor.parking_extractor import extract_parking
from extractor.property_subtype_extractor import extract_property_subtype
from extractor.metadata_extractor import extract_metadata
builder = StateGraph(GraphState)
builder.add_node("clean_text", clean_text_node)
builder.add_node("extract_request_type", extract_type)
builder.add_node("extract_bhk", extract_bhk)
builder.add_node("response", response_node)
builder.add_node("extract_price", extract_price)
builder.add_node("extract_location", extract_location)
builder.add_node("extract_furnishing", extract_furnishing)
builder.add_node("extract_facing", extract_facing)
builder.add_node("extract_parking", extract_parking)
builder.add_node("extract_amenities", extract_amenities)
builder.add_node("extract_property_subtype",extract_property_subtype)
builder.add_node("extract_metadata", extract_metadata)
builder.set_entry_point("clean_text")

builder.add_edge("clean_text", "extract_request_type")
builder.add_edge("clean_text", "extract_bhk")
builder.add_edge("clean_text","extract_metadata")
builder.add_edge("clean_text", "extract_location")
builder.add_edge("clean_text", "extract_furnishing")
builder.add_edge("clean_text", "extract_facing")
builder.add_edge("clean_text", "extract_parking")
builder.add_edge("clean_text", "extract_amenities")
builder.add_edge("clean_text", "extract_property_subtype")
builder.add_edge("extract_request_type", "extract_price")
builder.add_edge(["extract_request_type", "extract_bhk", "extract_price", "extract_location", "extract_furnishing", "extract_facing", "extract_parking", "extract_amenities", "extract_property_subtype", "extract_metadata"], "response")
builder.add_edge("response", END)

graph = builder.compile()

if __name__ == "__main__":
    png_data = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_data)

    result = graph.invoke({
        "user_input": """🏠REQUIRED 1 BHK FLAT FOR OUT RATE BUDGET 1 CR TO 1.10 CR
LOCATION ANY CHARKOP SECTOR
KANDIVALI WEST
Big swiming pool 
inbuild gym 
CALL
9820067788
CONTACT PERSON SURESH"""
    })
    structured_output = result.get("response_output")

    print("\nFinal Structured Output:")
    print(json.dumps(structured_output, indent=2, ensure_ascii=False))