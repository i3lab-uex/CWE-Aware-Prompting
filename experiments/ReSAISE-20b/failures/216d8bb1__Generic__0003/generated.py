# access_invoice.py

from typing import Dict, Any

# Example role definitions – in a real system these would come from a database or config
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

# Example invoice data – in a real system these would be stored securely
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.00, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": "INV-1002", "amount": 125.50, "items": ["Widget C"]},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for a given client if the requesting user has permission.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access the invoice.
    client_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice details if access is permitted; otherwise, the string 'Unauthorized'.

    Notes
    -----
    - Users with role "admin" can access any invoice.
    - Customers can only access their own invoices (user_id == client_id).
    - If the invoice does not exist, 'Unauthorized' is returned to avoid leaking existence.
    """
    # Verify that the user exists
    role = USER_ROLES.get(user_id)
    if not role:
        return "Unauthorized"

    # Check permissions
    is_admin = role.lower() == "admin"
    owns_invoice = user_id == client_id

    if not (is_admin or owns_invoice):
        return "Unauthorized"

    # Retrieve the invoice safely; if missing, treat as unauthorized
    invoice = INVOICES.get(client_id)
    return invoice or "Unauthorized"