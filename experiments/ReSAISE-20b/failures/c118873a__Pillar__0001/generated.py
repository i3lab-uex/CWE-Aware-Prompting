from typing import Dict, List, Any

# Example data structures (replace with real data in production)
USER_ROLES: Dict[int, List[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.00, "status": "Paid"},
    3: {"invoice_id": "INV-1002", "amount": 150.00, "status": "Pending"},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve the invoice for a given customer if the logged-in user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        ID of the user attempting to access the invoice.
    invoice_owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is allowed, otherwise the string 'Unauthorized'.
    """
    # Basic type checks to guard against injection or malformed input
    if not isinstance(logged_in_user_id, int) or not isinstance(invoice_owner_id, int):
        return "Unauthorized"

    # Determine if the user is an admin
    roles = USER_ROLES.get(logged_in_user_id, [])
    is_admin = "admin" in [role.lower() for role in roles]

    # User may access the invoice if they are admin or owner
    authorized = is_admin or logged_in_user_id == invoice_owner_id

    if not authorized:
        return "Unauthorized"

    # Fetch the invoice data; if none exists, treat as unauthorized
    invoice = INVOICES.get(invoice_owner_id)
    return invoice if invoice is not None else "Unauthorized"