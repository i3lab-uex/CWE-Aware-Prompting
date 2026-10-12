# view_order.py

"""
This module implements the `view_order` function for an e-commerce system.
It performs strict authorization checks to prevent CWE-863 (Incorrect
Authorization). Only admins can view any order, while customers may only view
orders they placed themselves.
"""

from __future__ import annotations

# Sample in‑memory database of orders
ORDERS_DB = {
    "order_001": {"order_id": "order_001", "user_id": "cust_a", "details": {"items": ["book"], "total": 12.99}},
    "order_002": {"order_id": "order_002", "user_id": "cust_b", "details": {"items": ["pen"], "total": 1.49}},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> dict:
    """
    Return the details of an order if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the user ('admin' or 'customer'). Case‑insensitive.
    order_id : str
        ID of the order to view.
    order_user_id : str
        The user ID that originally placed the order.

    Returns
    -------
    dict
        The full order record.

    Raises
    ------
    ValueError
        If the order does not exist.
    PermissionError
        If the user is not authorized to view the order.
    """

    # Normalize role for case‑insensitivity
    normalized_role = user_role.strip().lower()

    # 1. Verify the order exists
    order_record = ORDERS_DB.get(order_id)
    if not order_record:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # 2. Ensure consistency between passed order_user_id and the stored one
    if order_record["user_id"] != order_user_id:
        raise ValueError("Provided order_user_id does not match the record.")

    # 3. Authorization check
    if normalized_role == "admin":
        # Admins can view any order
        return order_record

    if normalized_role == "customer":
        # Customers may only view their own orders
        if user_id != order_user_id:
            raise PermissionError("Customers can only view their own orders.")
        return order_record

    # 4. If role is unrecognized, deny access
    raise PermissionError(f"Unrecognized user role '{user_role}'. Access denied.")


# Example usage (uncomment to test):
# try:
#     order = view_order("cust_a", "customer", "order_001", "cust_a")
#     print(order)
# except Exception as e:
#     print(e)