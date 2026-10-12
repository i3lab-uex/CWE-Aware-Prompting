from typing import Dict, Any

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

# Example invoice mapping: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-002", "amount": 150.0, "items": ["widget A"]},
    3: {"invoice_id": "INV-003", "amount": 200.0, "items": ["widget B"]},
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Allow a user to download an invoice if authorized.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the request.
    customer_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string 'Unauthorized'.
    """
    # Fetch roles for the current user safely
    roles = USER_ROLES.get(current_user_id, set())

    # Check if the user is an admin or the owner of the invoice
    authorized = "admin" in roles or current_user_id == customer_id

    if not authorized:
        return "Unauthorized"

    # Retrieve invoice data safely
    invoice = INVOICES.get(customer_id)
    if invoice is None:
        return "Unauthorized"  # treat missing invoice as unauthorized

    return invoice