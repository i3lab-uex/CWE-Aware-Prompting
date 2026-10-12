# --------------------------------------------------
# Invoice retrieval module
# --------------------------------------------------

from typing import Any, Dict

# Sample data structures (replace with real data sources in production)
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 250.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 125.0, "status": "unpaid"},
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice if the requester has permission.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to fetch the invoice.
    owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if access is allowed, otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role 'admin') can fetch any invoice.
    * Customers can only fetch their own invoices.
    * Missing users or invoices result in 'Unauthorized' to avoid leaking information.
    """
    # Validate existence of requester
    requester_roles = USER_ROLES.get(requester_id)
    if requester_roles is None:
        return "Unauthorized"

    # Check admin privilege
    if "admin" in requester_roles:
        invoice = INVOICES.get(owner_id)
        return invoice if invoice is not None else "Unauthorized"

    # Non-admin: must be the owner
    if requester_id != owner_id:
        return "Unauthorized"

    invoice = INVOICES.get(owner_id)
    return invoice if invoice is not None else "Unauthorized"