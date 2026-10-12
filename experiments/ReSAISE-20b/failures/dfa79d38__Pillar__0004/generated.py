# -*- coding: utf-8 -*-
"""
Module providing order viewing functionality with proper authorization checks.
"""

from typing import Dict, Any

# Sample in-memory orders database
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "cust123",
                  "items": ["item_a", "item_b"], "total": 59.99},
    "order_002": {"order_id": "order_002", "user_id": "cust456",
                  "items": ["item_c"], "total": 15.00},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str,
               order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to view the order.
    user_role : str
        The role of the caller (e.g., 'admin', 'customer').
    order_id : str
        The ID of the order to be retrieved.
    order_user_id : str
        The user ID that placed the order (used for validation).

    Returns
    -------
    dict
        The full order details.

    Raises
    ------
    ValueError
        If the requested order does not exist.
    PermissionError
        If the caller is not authorized to view the order.
    """
    # 1. Verify that the requested order exists
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # 2. Authorization check
    # Admins can view any order.
    if user_role.lower() == "admin":
        return order

    # Customers can only view their own orders.
    if user_role.lower() == "customer":
        if order_user_id != order["user_id"]:
            raise PermissionError("You are not authorized to view this order.")
        return order

    # Any other role is denied.
    raise PermissionError("You do not have permission to view orders.")


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         details = view_order("cust123", "customer", "order_001", "cust123")
#         print(details)
#     except Exception as e:
#         print(e)