from typing import Any, Dict

# Example data structures (replace with real ones in production)
USER_ROLES: Dict[int, str] = {
    # user_id : role
    1: "admin",
    2: "customer",
    3: "customer",
}
INVOICES: Dict[int, Any] = {
    # user_id : invoice_data
    2: {"invoice_number": "INV-1001", "amount": 250.0, "status": "paid"},
    3: {"invoice_number": "INV-1002", "amount": 150.0, "status": "unpaid"},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Return the invoice data for `client_id` if the requesting `user_id`
    is authorized (either an admin or the same user).  Otherwise
    return 'Unauthorized'.

    Args:
        user_id (int): ID of the user making the request.
        client_id (int): ID of the customer whose invoice is requested.

    Returns:
        Any: Invoice data if authorized, else 'Unauthorized'.
    """
    # Fetch role; default to empty string if not found
    role = USER_ROLES.get(user_id, "")

    # Authorization check: admin or owner
    if role == "admin" or user_id == client_id:
        # Retrieve invoice; return None if not present
        return INVOICES.get(client_id)
    else:
        return "Unauthorized"