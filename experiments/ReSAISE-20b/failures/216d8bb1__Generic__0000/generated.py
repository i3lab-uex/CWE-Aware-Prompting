# access_invoice.py

from typing import Dict, Any, List

# Example role mapping and invoice storage.
# In a real system these would come from a database or external service.
USER_ROLES: Dict[int, List[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.0, "items": ["widget A", "widget B"]},
    3: {"invoice_id": "INV-1002", "amount": 125.0, "items": ["widget C"]},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Return the invoice data for *client_id* if *user_id* is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access an invoice.
    client_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role contains 'admin') may access any invoice.
    * Customers may only access their own invoice.
    """
    # Validate that the user exists in our role mapping
    if user_id not in USER_ROLES:
        return "Unauthorized"

    # Determine whether the user is an administrator
    roles = set(USER_ROLES[user_id])
    is_admin = "admin" in roles

    # Check if the requested invoice exists
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    # Authorization logic
    if is_admin or user_id == client_id:
        return invoice

    return "Unauthorized"