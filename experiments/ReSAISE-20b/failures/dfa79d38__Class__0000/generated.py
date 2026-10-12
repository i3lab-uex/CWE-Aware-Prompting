# -*- coding: utf-8 -*-

"""
Order viewing module.

This module defines the `view_order` function that allows a user to retrieve
the details of an order. Authorization is performed according to the
following rules:

* An 'admin' user can view any order.
* A 'customer' user may only view orders that belong to them.
"""

from __future__ import annotations

# Sample in‑memory order database. In a real application this would be
# replaced with persistent storage (e.g., a relational database).
ORDERS_DB: dict[str, dict] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_a", "details": {"items": ["apple", "banana"], "total": 12.5}},
    "order_002": {"order_id": "order_002", "user_id": "cust_b", "details": {"items": ["orange"], "total": 5.0}},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> dict:
    """
    Return the details of a specific order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the user (e.g., 'admin' or 'customer').
    order_id : str
        ID of the order to be viewed.
    order_user_id : str
        The user ID associated with the order (should match ORDERS_DB entry).

    Returns
    -------
    dict
        The order details dictionary.

    Raises
    ------
    ValueError
        If the order does not exist in ORDERS_DB.
    PermissionError
        If the user is not authorized to view the order.

    Notes
    -----
    * The function performs a strict equality check on `order_user_id` against the
      stored value to avoid tampering.
    * The role check is case‑insensitive to reduce accidental failures.
    """
    # Retrieve the order from the database
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # Verify that the provided order_user_id matches the stored one
    if order_user_id != order["user_id"]:
        raise ValueError("Provided user ID does not match the order's owner.")

    # Authorization logic
    role = user_role.strip().lower()
    if role == "admin":
        # Admins can view any order
        pass
    elif role == "customer":
        if user_id != order_user_id:
            raise PermissionError("Customers can only view their own orders.")
    else:
        # Unknown roles are treated as unauthorized
        raise PermissionError(f"Unknown role '{user_role}'. Access denied.")

    # Return a copy to prevent accidental modification of the internal DB
    return dict(order)


# Example usage (uncomment for testing):
# if __name__ == "__main__":
#     try:
#         print(view_order("cust_a", "customer", "order_001", "cust_a"))
#     except Exception as e:
#         print(f"Error: {e}")