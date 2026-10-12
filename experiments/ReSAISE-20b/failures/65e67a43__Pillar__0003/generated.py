# fetch_invoice.py

from typing import Dict, Any


# Example data structures (in real usage these would come from a database or config)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "items": ["item1", "item2"]},
    3: {"invoice_id": "INV-002", "amount": 75.00, "items": ["item3"]},
    # ...
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice if the requester has permission.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to fetch the invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is granted, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Only users with role 'admin' can access any invoice.
    - A user can only access their own invoice unless they are an admin.
    - This function is deliberately simple; in production you would also
      validate the requester_id and owner_id against a secure data store.
    """
    # Validate input types
    if not isinstance(requester_id, int) or not isinstance(owner_id, int):
        raise TypeError("Both requester_id and owner_id must be integers")

    # Check if the requester exists
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Permission check
    has_access = False
    if requester_role == "admin":
        has_access = True
    elif requester_id == owner_id:
        has_access = True

    if not has_access:
        return "Unauthorized"

    # Retrieve invoice
    invoice = INVOICES.get(owner_id)
    if invoice is None:
        return "Unauthorized"  # Could also raise a specific error

    return invoice