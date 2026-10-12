# -*- coding: utf-8 -*-
"""
A minimal e‑commerce order viewing module that demonstrates proper
authorization checks.
"""

from typing import Dict

# Sample in‑memory orders database
ORDERS_DB: Dict[str, Dict] = {
    "order_001": {"id": "order_001", "user_id": "cust_a", "items": ["book", "pen"]},
    "order_002": {"id": "order_002", "user_id": "cust_b", "items": ["laptop"]},
    # Add more orders as needed
}


def view_order(user_id: str, user_role: str, order_id: str,
               order_user_id: str) -> Dict:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to view the order.
    user_role : str
        Role of the user (e.g., 'admin' or 'customer').
    order_id : str
        Identifier of the order to be viewed.
    order_user_id : str
        The ID of the user who placed the order.

    Returns
    -------
    dict
        Order details from ``ORDERS_DB``.

    Raises
    ------
    ValueError
        If the order does not exist in ``ORDERS_DB``.
    PermissionError
        If the user is not authorized to view the order.

    Notes
    -----
    * The function first validates that the requested ``order_id`` exists.
      This protects against a potential CWE‑863 (incorrect authorization)
      by ensuring that the existence check occurs before any
      authorization logic.
    * Authorization is performed with strict equality checks to avoid
      accidental privilege escalation due to type coercion or malformed input.
    """
    # 1. Verify that the order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order '{order_id}' does not exist.")

    # 2. Authorization check
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
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to view order '{order_id}'."
        )

    # 3. Return the order details
    return ORDERS_DB[order_id]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         order = view_order("cust_a", "customer", "order_001", "cust_a")
#         print(order)
#     except Exception as e:
#         print(e)