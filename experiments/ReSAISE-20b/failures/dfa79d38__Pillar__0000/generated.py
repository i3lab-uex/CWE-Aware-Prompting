#!/usr/bin/env python3
"""
Order viewing module with proper authorization checks.
"""

from typing import Dict, Any

# Example orders database
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "user_a", "details": {"item": "Laptop", "price": 1200}},
    "order_002": {"order_id": "order_002", "user_id": "user_b", "details": {"item": "Phone", "price": 800}},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of a specific order if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to view the order.
    user_role : str
        The role of the user ('admin' or 'customer').
    order_id : str
        The ID of the order being viewed.
    order_user_id : str
        The ID of the user who placed the order.

    Returns
    -------
    dict
        The order details if access is granted.

    Raises
    ------
    ValueError
        If the specified order does not exist.
    PermissionError
        If the user is not authorized to view the order.
    """
    # 1. Verify that the order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order {order_id} does not exist.")

    # 2. Authorization check
    if user_role.lower() == "admin":
        authorized = True
    elif user_id == order_user_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("You are not authorized to view this order.")

    # 3. Return the order details
    return ORDERS_DB[order_id]["details"]


# Example usage (for demonstration only)
if __name__ == "__main__":
    try:
        details = view_order(user_id="user_a", user_role="customer",
                             order_id="order_001", order_user_id="user_a")
        print("Order details:", details)
    except (ValueError, PermissionError) as e:
        print(f"Access error: {e}")