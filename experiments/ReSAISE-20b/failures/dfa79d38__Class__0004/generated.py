# -*- coding: utf-8 -*-
"""
E-commerce order viewing module.

This module contains the `view_order` function that enforces proper
authorization checks before returning order details. It follows best
practices to avoid CWE-863 (Incorrect Authorization) by ensuring that
only administrators or the user who placed the order can view it.
"""

from typing import Dict, Any

# Sample in-memory orders database. In a real application this would
# be replaced by persistent storage (e.g., SQL, NoSQL, or an ORM).
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "user_a",
                  "items": [{"sku": "ABC123", "qty": 2}], "total": 49.99},
    "order_002": {"order_id": "order_002", "user_id": "user_b",
                  "items": [{"sku": "XYZ789", "qty": 1}], "total": 19.99},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str,
               order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the caller (e.g., 'admin', 'customer').
    order_id : str
        Identifier of the requested order.
    order_user_id : str
        User ID who placed the order (redundant, but used for safety).

    Returns
    -------
    dict
        Order details.

    Raises
    ------
    ValueError
        If the order does not exist in `ORDERS_DB`.
    PermissionError
        If the caller is not authorized to view the order.
    """
    # 1. Verify that the order exists
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order {order_id} does not exist")

    # 2. Enforce strict authorization
    #    - Admins can view any order.
    #    - Customers can only view their own orders.
    if user_role == "admin":
        authorized = True
    elif user_role == "customer":
        # Ensure the provided order_user_id matches the stored one
        authorized = (order_user_id == order["user_id"])
    else:
        # Unknown roles are denied by default
        authorized = False

    if not authorized:
        raise PermissionError("You do not have permission to view this order")

    # 3. Return a copy of the order data to prevent accidental mutation
    return dict(order)