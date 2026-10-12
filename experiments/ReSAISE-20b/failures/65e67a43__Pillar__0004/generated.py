# -*- coding: utf-8 -*-
"""
Implements an access‑controlled invoice retrieval function.

The function ensures that only the owner of an invoice or a user with
the ``admin`` role may access it.  It follows best practices to avoid
CWE‑284 (Improper Access Control) by validating roles and checking
object ownership before returning sensitive data.
"""

from typing import Any, Dict

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice storage: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.50, "status": "unpaid"},
}

def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to retrieve the invoice.
    owner_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice details if access is permitted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Only users with the role ``admin`` or the invoice owner may access
      the invoice.
    - If either user ID is unknown, or if the invoice does not exist,
      access is denied.
    """
    # Basic input validation
    if not isinstance(requester_id, int) or not isinstance(owner_id, int):
        return "Unauthorized"

    # Retrieve roles for the requester
    requester_roles = USER_ROLES.get(requester_id, [])

    # Check ownership or admin privilege
    is_owner = requester_id == owner_id
    is_admin = "admin" in requester_roles

    if not (is_owner or is_admin):
        return "Unauthorized"

    # Fetch the invoice; ensure it exists
    invoice = INVOICES.get(owner_id)
    if invoice is None:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    return dict(invoice)

# Example usage (uncomment for testing)
# print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
# print(fetch_invoice(2, 2))   # Owner accessing own invoice
# print(fetch_invoice(3, 2))   # Unauthorized access attempt