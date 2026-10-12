from typing import Any, Dict

# Example role mapping: user_id -> list of roles (e.g., ["admin"], ["customer"])
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice data mapping: user_id -> invoice details
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
}

def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access the invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice details if access is permitted, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Only users with role 'admin' can access any invoice.
    - Customers may only view their own invoices.
    """
    # Retrieve the requester's roles safely
    requester_roles = USER_ROLES.get(requester_id, [])

    # Determine if access is allowed
    if "admin" in requester_roles or requester_id == owner_id:
        # Return a copy to prevent accidental modification of the stored data
        return INVOICES.get(owner_id, {}).copy()
    else:
        return "Unauthorized"