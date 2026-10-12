from typing import Dict, Any

# Example role mapping: user_id -> set of roles (e.g., {"admin"}, {"customer"})
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

# Example invoice storage: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "date": "2024-06-01"},
    3: {"invoice_id": "INV-002", "amount": 75.00,  "date": "2024-06-02"},
}

def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice if the requester has proper authorization.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access an invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are an administrator or if they own the invoice.
    - Role checks use set membership to avoid accidental key errors.
    """
    # Verify that both users exist in the role mapping
    requester_roles = USER_ROLES.get(requester_id, set())
    if not requester_roles:
        return "Unauthorized"

    # Allow access if requester is an admin or the owner of the invoice
    if "admin" in requester_roles or requester_id == owner_id:
        return INVOICES.get(owner_id, "Unauthorized")

    # Deny access otherwise
    return "Unauthorized"