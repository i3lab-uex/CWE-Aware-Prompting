# -*- coding: utf-8 -*-

"""
E-commerce order viewing module.
"""

from __future__ import annotations

# Example orders database (in a real system this would be a persistent store)
ORDERS_DB: dict[str, dict] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_123", "details": {"items": ["apple", "banana"], "total": 15.50}},
    "order_002": {"order_id": "order_002", "user_id": "cust_456", "details": {"items": ["orange"], "total": 5.25}},
    # ... more orders ...
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> dict:
    """
    Retrieve the details of a specific order if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the requesting user (e.g., 'admin' or 'customer').
    order_id : str
        Identifier of the order to be retrieved.
    order_user_id : str
        ID of the user who placed the order (as stored in ORDERS_DB).

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

    Notes
    -----
    - Admin users can view any order.
    - Customers may only view orders that belong to them.
    """
    # 1. Validate the order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # 2. Perform authorization checks
    if user_role.lower() == "admin":
        # Admins have full access
        return ORDERS_DB[order_id]

    if user_role.lower() == "customer":
        # Customers can only view their own orders
        if user_id != order_user_id:
            raise PermissionError("You are not authorized to view this order.")
        return ORDERS_DB[order_id]

    # 3. Unsupported roles
    raise PermissionError(f"Role '{user_role}' is not permitted to view orders.")


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         order = view_order("cust_123", "customer", "order_001", "cust_123")
#         print(order)
#     except Exception as e:
#         print(f"Error: {e}")