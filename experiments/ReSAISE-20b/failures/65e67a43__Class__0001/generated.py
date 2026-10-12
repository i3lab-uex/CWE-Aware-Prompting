# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module defines the `fetch_invoice` function, which returns a customer's
invoice data if and only if the requester is authorized to access it.
Authorization rules:
  * Administrators (role 'admin') may retrieve any invoice.
  * Customers may only retrieve their own invoice.

The function is intentionally defensive against common security pitfalls
such as missing authorization checks (CWE‑862) and data leakage.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example user-role mapping (in a real system this would come from a DB or
# an authentication service).  For the purpose of this module we keep it
# simple and static.
#
#   USER_ROLES: user_id -> set of roles (e.g., {"admin"} or {"customer"})
# --------------------------------------------------------------------------- #
USER_ROLES = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
    # ... additional users
}

# --------------------------------------------------------------------------- #
# Example invoice storage (in a real system this would be persisted in a
# database or a secure file store).  Each invoice is represented as a dict.
#
#   INVOICES: user_id -> invoice data
# --------------------------------------------------------------------------- #
INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 120.00, "status": "Paid"},
    3: {"invoice_id": "INV-002", "amount": 75.50, "status": "Unpaid"},
    # ... additional invoices
}


def fetch_invoice(requester_id: int, owner_id: int) -> dict | str:
    """
    Retrieve the invoice data for a given customer if the requester is
    authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to retrieve an invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice details if the requester is authorized; otherwise
        the string 'Unauthorized'.

    Notes
    -----
    * The function performs an explicit authorization check to guard
      against CWE‑862 (Missing Authorization).
    * It avoids leaking sensitive information by returning a generic
      'Unauthorized' message on failure.
    """
    # Validate input types early to avoid accidental misuse
    if not isinstance(requester_id, int) or not isinstance(owner_id, int):
        raise TypeError("requester_id and owner_id must be integers")

    # --------------------------------------------------------------------- #
    # Authorization logic
    # --------------------------------------------------------------------- #
    requester_roles = USER_ROLES.get(requester_id, set())

    is_admin = "admin" in requester_roles
    is_owner = requester_id == owner_id

    if not (is_admin or is_owner):
        # Deny access explicitly
        return "Unauthorized"

    # --------------------------------------------------------------------- #
    # Fetch the invoice data.  If the owner has no invoice, we return a
    # meaningful error message instead of leaking that information.
    # --------------------------------------------------------------------- #
    invoice = INVOICES.get(owner_id)
    if invoice is None:
        return f"No invoice found for user {owner_id}"

    # Return a copy to prevent accidental mutation of the global state
    return invoice.copy()


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove or guard under __main__ in
# production code)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
    print(fetch_invoice(2, 2))   # Customer accessing own invoice
    print(fetch_invoice(3, 2))   # Unauthorized access attempt