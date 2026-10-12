from typing import Any, Dict

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice data: user_id -> invoice details
INVOICES: Dict[int, dict] = {
    2: {"invoice_id": "INV-001", "amount": 120.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 75.5, "status": "unpaid"},
}

def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access the invoice.
    customer_request_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized; otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if requester_id not in USER_ROLES or customer_request_id not in INVOICES:
        return "Unauthorized"

    # Check if the requester is an admin
    roles = USER_ROLES.get(requester_id, [])
    if "admin" in roles:
        # Admins can access any invoice
        return INVOICES[customer_request_id].copy()

    # If the requester is not an admin, they must be requesting their own invoice
    if requester_id == customer_request_id:
        return INVOICES[customer_request_id].copy()

    # Any other case is unauthorized
    return "Unauthorized"