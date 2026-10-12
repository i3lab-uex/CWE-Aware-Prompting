# view_order.py

from typing import Dict, Any


# Example in‑memory orders database. In a real system this would be replaced
# with a persistent store (e.g., SQL, NoSQL).
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"id": "order_001", "user_id": "cust123", "details": {"items": ["book"], "total": 29.99}},
    "order_002": {"id": "order_002", "user_id": "cust456", "details": {"items": ["pen"], "total": 5.49}},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the caller (e.g., 'admin' or 'customer').
    order_id : str
        ID of the order to be viewed.
    order_user_id : str
        User ID associated with the order (should match ORDERS_DB[order_id]['user_id']).

    Returns
    -------
    Dict[str, Any]
        The full order record from ORDERS_DB.

    Raises
    ------
    ValueError
        If the specified order does not exist in ORDERS_DB.
    PermissionError
        If the caller is not authorized to view the order.
    """

    # 1. Validate that the order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order '{order_id}' does not exist.")

    # 2. Retrieve the stored order record
    order_record = ORDERS_DB[order_id]

    # 3. Ensure the provided order_user_id matches the stored one
    if order_record["user_id"] != order_user_id:
        raise ValueError("Order user ID mismatch.")

    # 4. Authorization check
    if user_role.lower() == "admin":
        # Admins can view any order
        authorized = True
    elif user_id == order_user_id:
        # Customers can view only their own orders
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("You are not authorized to view this order.")

    # 5. Return a copy of the order record to avoid accidental mutation
    return dict(order_record)


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         order = view_order(user_id="cust123", user_role="customer",
#                            order_id="order_001", order_user_id="cust123")
#         print(order)
#     except Exception as e:
#         print(f"Error: {e}")