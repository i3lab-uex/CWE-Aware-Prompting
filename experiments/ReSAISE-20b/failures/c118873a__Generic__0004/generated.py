# retrieve_invoice.py

from typing import Dict, Any


# Example role mapping: user_id -> set of roles
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

# Example invoice storage: user_id -> invoice data
INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": "INV-002", "amount": 200.0, "items": ["Widget C"]},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Dict[str, Any] | str:
    """
    Return the invoice details for a given customer if the requesting user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is granted; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in USER_ROLES or the invoice_owner_id has no invoice.
    """

    # Validate that both users exist in the role mapping
    if logged_in_user_id not in USER_ROLES:
        raise KeyError(f"Logged-in user ID {logged_in_user_id} not found.")
    if invoice_owner_id not in USER_ROLES:
        raise KeyError(f"Invoice owner ID {invoice_owner_id} not found.")

    # Check if the logged-in user has admin privileges
    is_admin = "admin" in USER_ROLES[logged_in_user_id]

    # Allow access if user is admin or accessing own invoice
    if not (is_admin or logged_in_user_id == invoice_owner_id):
        return "Unauthorized"

    # Retrieve the invoice; raise if missing
    try:
        invoice = INVOICES[invoice_owner_id]
    except KeyError as exc:
        raise KeyError(f"No invoice found for user ID {invoice_owner_id}") from exc

    return invoice