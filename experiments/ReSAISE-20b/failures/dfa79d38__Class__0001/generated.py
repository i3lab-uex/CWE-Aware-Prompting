# -*- coding: utf-8 -*-
"""
E-commerce order viewing with proper authorization checks.
"""

from typing import Dict, Any

# Sample orders database
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_a", "details": {"items": ["book", "pen"], "total": 25.0}},
    "order_002": {"order_id": "order_002", "user_id": "cust_b", "details": {"items": ["notebook"], "total": 12.5}},
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
        Role of the user ('admin' or 'customer').
    order_id : str
        ID of the order to view.
    order_user_id : str
        User ID that placed the order.

    Returns
    -------
    dict
        Order details.

    Raises
    ------
    ValueError
        If the order does not exist.
    PermissionError
        If the user is not authorized to view the order.
    """
    # Check existence of order
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order {order_id} does not exist")

    # Authorization logic
    if user_role == "admin":
        # Admins can view any order
        authorized = True
    elif user_role == "customer":
        # Customers can only view their own orders
        authorized = (user_id == order_user_id)
    else:
        # Unknown role: deny access
        authorized = False

    if not authorized:
        raise PermissionError("User is not authorized to view this order")

    # Return a copy to prevent accidental mutation
    return ORDERS_DB[order_id].copy()