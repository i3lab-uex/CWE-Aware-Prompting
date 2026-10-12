import json
from typing import Dict, Any

# Example in‑memory orders database.
# Each order is stored as a dict with keys: 'order_id', 'user_id', and 'details'.
ORDERS_DB: Dict[str, Dict[str, Any]] = {
    "order123": {
        "order_id": "order123",
        "user_id": "cust01",
        "details": {
            "items": [
                {"sku": "ABC123", "qty": 2, "price": 19.99},
                {"sku": "XYZ789", "qty": 1, "price": 49.99},
            ],
            "total": 89.97,
            "status": "shipped",
        },
    },
    # Additional orders can be added here.
}


def view_order(
    user_id: str,
    user_role: str,
    order_id: str,
    order_user_id: str,
) -> Dict[str, Any]:
    """
    Return the details of an order if the requesting user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to view the order.
    user_role : str
        Role of the user ('admin' or 'customer').
    order_id : str
        ID of the order to be viewed.
    order_user_id : str
        The user ID that originally placed the order.

    Returns
    -------
    dict
        Order details if access is granted.

    Raises
    ------
    ValueError
        If the order does not exist.
    PermissionError
        If the user is not authorized to view the order.
    """
    # 1. Check if the order exists
    order = ORDERS_DB.get(order_id)
    if not order:
        raise ValueError(f"Order with ID '{order_id}' does not exist.")

    # 2. Authorization logic
    if user_role == "admin":
        # Admins can view any order.
        authorized = True
    elif user_role == "customer":
        # Customers can only view their own orders.
        authorized = order_user_id == user_id
    else:
        # Unknown roles are not permitted.
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized "
            f"to view order '{order_id}'."
        )

    # 3. Return a deep copy to prevent accidental mutation of the DB.
    return json.loads(json.dumps(order))


# Example usage:
if __name__ == "__main__":
    try:
        details = view_order(
            user_id="cust01",
            user_role="customer",
            order_id="order123",
            order_user_id="cust01",
        )
        print("Order details:", json.dumps(details, indent=2))
    except Exception as e:
        print(str(e))