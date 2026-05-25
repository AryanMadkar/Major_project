from .GraphState import GraphState
# =========================
# RESPONSE NODE
# =========================
def response_node(state: GraphState):

    bhk = state.get("bhk")

    if bhk is not None:
        print(f"Detected BHK: {bhk}")
    else:
        print("No BHK found")
    if state.get("request_type"):
        print(f"Detected Request Type: {state['request_type']}")
    else:
        print("No Request Type found")
    if state.get("cleaned_text"):
        print(f"Cleaned Text: {state['cleaned_text']}")
    else:
        print("No Cleaned Text found")
    

    return state