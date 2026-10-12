import typing as _t

# Sample in‑memory orders database.
# In a real system this would be replaced with a proper persistence layer (e.g., SQL, NoSQL).
ORDERS_DB: dict[str, dict] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_123", "items": ["book", "pen"], "total": 25.5},
    "order_002": {"order_id": "order_002", "user_id": "cust_456", "items": ["laptop"], "total": 999.99},
    # ... more orders
}


def view_order(
    user_id: str,
    user_role: str,
    order_id: str,
    order_user_id: str,
) -> dict:
    """
    Return the details of an order if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user making the request.
    user_role : str
        Role of the user (`'admin'` or `'customer'`).
    order_id : str
        ID of the order to view.
    order_user_id : str
        User ID that originally placed the order.

    Returns
    -------
    dict
        Order details dictionary.

    Raises
    ------
    ValueError
        If the order does not exist in ``ORDERS_DB``.
    PermissionError
        If the user is not authorized to view the order.

    Notes
    -----
    * Admins can view any order.
    * Customers can only view orders that belong to them.
    """
    # Check existence first
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # Authorization logic
    if user_role.lower() == "admin":
        authorized = True
    elif user_role.lower() == "customer" and user_id == order_user_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to view order '{order_id}'."
        )

    # Return a copy to avoid accidental mutation of the in‑memory DB
    return dict(order)


# Example usage (uncomment to test):
# try:
#     print(view_order("cust_123", "customer", "order_001", "cust_123"))
#     print(view_order("cust_456", "customer", "order_001", "cust_123"))
# except Exception as e:
#     print(e)