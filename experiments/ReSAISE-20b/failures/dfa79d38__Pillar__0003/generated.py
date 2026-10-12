# -*- coding: utf-8 -*-
"""
Module: order_viewer

Provides a secure function to view an e‑commerce order.
"""

from typing import Dict, Any


# Example orders database
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_123",
                  "items": ["book", "pen"], "total": 25.50},
    "order_002": {"order_id": "order_002", "user_id": "cust_456",
                  "items": ["laptop"], "total": 1200.00},
    # ... additional orders ...
}


def view_order(user_id: str, user_role: str,
               order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to view the order.
    user_role : str
        Role of the caller (e.g., 'admin' or 'customer').
    order_id : str
        The ID of the order to view.
    order_user_id : str
        The user ID associated with the order.

    Returns
    -------
    dict
        Order details.

    Raises
    ------
    ValueError
        If the order does not exist in ORDERS_DB.
    PermissionError
        If the caller is not authorized to view the order.
    """
    # Ensure the order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order '{order_id}' does not exist.")

    # Authorization check
    if user_role.lower() == "admin":
        authorized = True
    else:
        authorized = (user_id == order_user_id)

    if not authorized:
        raise PermissionError("User is not authorized to view this order.")

    # Return a copy to prevent accidental mutation
    return dict(ORDERS_DB[order_id])


# Example usage (commented out for module integrity)
if __name__ == "__main__":
    try:
        details = view_order("cust_123", "customer",
                             "order_001", "cust_123")
        print(details)
    except (ValueError, PermissionError) as e:
        print(f"Access denied: {e}")