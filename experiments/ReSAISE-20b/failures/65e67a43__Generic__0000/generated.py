from typing import Any, Dict

# Example data structures – replace with real data in production
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "date": "2024-07-01"},
    3: {"invoice_id": 102, "amount": 175.50, "date": "2024-06-15"},
    # ... other invoices
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve the invoice for a customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to access the invoice.
    owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is granted; otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - Users with the role 'admin' can access any invoice.
    - If either user ID is unknown, access is denied.
    """
    # Check that both users exist in the system
    if requester_id not in USER_ROLES or owner_id not in INVOICES:
        return "Unauthorized"

    # Admins can access any invoice
    if USER_ROLES.get(requester_id) == "admin":
        return INVOICES[owner_id]

    # Users can access only their own invoice
    if requester_id == owner_id:
        return INVOICES[owner_id]

    # All other cases are unauthorized
    return "Unauthorized"