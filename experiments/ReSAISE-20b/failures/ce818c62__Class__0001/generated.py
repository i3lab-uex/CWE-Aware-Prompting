from typing import Any, Dict

# Example role mapping: user_id -> set of roles
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
    # add more users as needed
}

# Example invoice mapping: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
    # add more invoices as needed
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Allow a user to download an invoice if they are authorized.

    Args:
        current_user_id (int): The ID of the user making the request.
        customer_id (int): The ID of the customer whose invoice is requested.

    Returns:
        Any: Invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Verify that both users exist in our system
    if current_user_id not in USER_ROLES or customer_id not in INVOICES:
        return "Unauthorized"

    # Determine if the requester is an admin
    is_admin = "admin" in USER_ROLES.get(current_user_id, set())

    # Allow download if requester is admin or requesting their own invoice
    if not (is_admin or current_user_id == customer_id):
        return "Unauthorized"

    # Return the requested invoice data
    return INVOICES[customer_id]