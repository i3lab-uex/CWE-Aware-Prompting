from __future__ import annotations

# Sample in‑memory orders database. In a real application this would be
# backed by a persistent store.
ORDERS_DB: dict[str, dict] = {
    "order_001": {"order_id": "order_001", "user_id": "cust_123", "details": {"items": 3, "total": 59.99}},
    "order_002": {"order_id": "order_002", "user_id": "cust_456", "details": {"items": 1, "total": 19.99}},
    # ... more orders ...
}

def view_order(user_id: str, user_role: str, order_id: str, order_user_id: str) -> dict:
    """
    Return the details of an order if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user making the request.
    user_role : str
        Role of the requesting user (e.g., 'admin', 'customer').
    order_id : str
        ID of the order to view.
    order_user_id : str
        User ID that placed the order (must match ORDERS_DB entry).

    Returns
    -------
    dict
        The full order record.

    Raises
    ------
    ValueError
        If the requested order does not exist.
    PermissionError
        If the user is not authorized to view the order.

    Notes
    -----
    * Admin users can view any order.
    * Customer users may only view orders that belong to them.
    """
    # 1. Verify the order exists
    order = ORDERS_DB.get(order_id)
    if order is None:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # 2. Basic consistency check: the caller-provided order_user_id must match DB
    if order["user_id"] != order_user_id:
        raise ValueError("Provided order_user_id does not match the stored user ID for this order.")

    # 3. Authorization checks
    if user_role.lower() == "admin":
        # Admins have full access
        return order

    if user_role.lower() == "customer":
        # Customers can only view their own orders
        if user_id != order_user_id:
            raise PermissionError("You are not authorized to view this order.")
        return order

    # If the role is unknown, deny access
    raise PermissionError(f"Unknown user role '{user_role}'. Access denied.")