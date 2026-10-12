# orders.py

from typing import Dict, Any


# Sample in‑memory database of orders.
# In a real system this would be replaced by persistent storage.
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order_001": {"order_id": "order_001", "user_id": "user_a", "items": ["apple", "banana"], "total": 15.0},
    "order_002": {"order_id": "order_002", "user_id": "user_b", "items": ["orange"], "total": 5.0},
    # Add more orders as needed.
}


def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> Dict[str, Any]:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the caller (e.g., 'admin', 'customer').
    order_id : str
        ID of the order to retrieve.
    order_user_id : str
        The user ID that placed the order.

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
    # Check that the requested order exists
    if order_id not in ORDERS_DB:
        raise ValueError(f"Order '{order_id}' does not exist.")

    # Authorization logic
    if user_role.lower() == "admin":
        # Admins can view any order
        authorized = True
    elif user_role.lower() == "customer":
        # Customers can only view their own orders
        authorized = user_id == order_user_id
    else:
        # Unknown roles are not permitted
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to view order '{order_id}'."
        )

    # Return a copy of the order details to avoid accidental mutation
    return ORDERS_DB[order_id].copy()