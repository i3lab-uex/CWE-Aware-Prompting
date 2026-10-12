from typing import Any, Dict

# Example data structures – in a real system these would come from a database or
# secure store.  They are defined here for the sake of completeness.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... additional users
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 250.00, "date": "2024-01-15"},
    3: {"invoice_id": "INV-002", "amount": 125.50, "date": "2024-01-20"},
    # ... additional invoices
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Return the invoice data for ``owner_id`` if the caller is authorized.
    Admin users can fetch any invoice; customers may only fetch their own.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to access an invoice.
    owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is permitted; otherwise the string
        'Unauthorized'.

    Raises
    ------
    TypeError
        If either ``requester_id`` or ``owner_id`` is not an integer.
    KeyError
        If the requested invoice does not exist for ``owner_id``.
    """
    # Basic type validation to avoid accidental injection of non‑integer IDs
    if not isinstance(requester_id, int) or not isinstance(owner_id, int):
        raise TypeError("Both requester_id and owner_id must be integers")

    # Determine the role of the requester
    role = USER_ROLES.get(requester_id)

    # Deny access if the user is unknown or not an admin
    if role != "admin" and requester_id != owner_id:
        return "Unauthorized"

    # Retrieve the invoice – will raise KeyError if it does not exist
    return INVOICES[owner_id]