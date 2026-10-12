# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

Provides a single public function `fetch_invoice` that allows
customers to download their own invoices and administrators
to download any invoice.  The function performs a simple role
check using the `USER_ROLES` mapping and returns the invoice data
from the `INVOICES` dictionary.

The implementation avoids side‑effects, uses type hints and
explicit error handling for missing data.
"""

from __future__ import annotations

# Example role mapping and invoice storage. In a real system these
# would be replaced by database lookups or an external service.
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: dict[int, dict] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 75.5, "status": "unpaid"},
    # ... other invoices
}


def fetch_invoice(requester_id: int, owner_id: int) -> dict | str:
    """
    Retrieve an invoice if the requester has permission.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to fetch an invoice.
    owner_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    dict | str
        The invoice data if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    * A user may fetch an invoice only if they are the owner or have
      the role 'admin'.
    * If either user ID is not present in ``USER_ROLES`` or the invoice
      does not exist, the function returns 'Unauthorized' to avoid
      leaking information about account existence.
    """
    # Validate requester role
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Check permission
    has_permission = requester_role == "admin" or requester_id == owner_id
    if not has_permission:
        return "Unauthorized"

    # Retrieve the invoice; absence implies unauthorized access
    invoice = INVOICES.get(owner_id)
    return invoice if invoice is not None else "Unauthorized"


# Example usage (commented out to keep module import‑friendly)
if __name__ == "__main__":
    print(fetch_invoice(1, 2))  # Admin fetching customer 2's invoice
    print(fetch_invoice(2, 3))  # Customer 2 attempting to fetch customer 3's invoice
    print(fetch_invoice(2, 2))  # Customer 2 fetching their own invoice