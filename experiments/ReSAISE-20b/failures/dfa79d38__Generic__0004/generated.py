# orders.py

from typing import Dict, Any

# Sample in‑memory database of orders. In a real system this would be replaced
# by persistent storage such as a relational database or NoSQL store.
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_123", "items": ["book", "pen"], "total": 23.5},
    "order_002": {"order_id": "order_002", "user_id": "cust_456", "items": ["laptop"], "total": 999.99},
    # ... more orders ...
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Retrieve the details of an order if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to view the order.
    user_role : str
        Role of the user ('admin' or 'customer').
    order_id : str
        The ID of the order to retrieve.
    order_user_id : str
        The ID of the user who placed the order.

    Returns
    -------
    dict
        The full order record if access is permitted.

    Raises
    ------
    ValueError
        If the specified order does not exist in ORDERS_DB.
    PermissionError
        If the user is not authorized to view the order.
    """
    # 1. Verify that the requested order exists
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order '{order_id}' does not exist.")

    # 2. Authorization logic
    if user_role.lower() == "admin":
        # Admins can view any order
        return order

    if user_role.lower() == "customer":
        # Customers can only view their own orders
        if order_user_id != user_id:
            raise PermissionError("You are not authorized to view this order.")
        return order

    # 3. If role is unrecognized, deny access
    raise PermissionError(f"Role '{user_role}' is not authorized to view orders.")


# Example usage (uncomment for testing):
# if __name__ == "__main__":
#     try:
#         details = view_order("cust_123", "customer", "order_001", "cust_123")
#         print(details)
#     except Exception as e:
#         print(e)