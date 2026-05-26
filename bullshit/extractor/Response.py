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

     # =====================================
    # PRICE
    # =====================================

    if state.get("price"):
        print(f"Detected Price: ₹{state['price']:,}")

    if state.get("rent_price"):
        print(f"Detected Rent: ₹{state['rent_price']:,}")

    if state.get("deposit_price"):
        print(f"Detected Deposit: ₹{state['deposit_price']:,}")

    if state.get("price_type"):
        print(f"Price Type: {state['price_type']}")
    

    return state