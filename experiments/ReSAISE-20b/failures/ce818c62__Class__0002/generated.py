#!/usr/bin/env python3
"""
Secure invoice download helper.

The module defines a single public function `download_invoice` that enforces
authorization based on the caller's role and ownership.  It protects against
CWE‑862 (Missing Authorization) by explicitly checking that the requesting user
is either:

* The owner of the invoice (`current_user_id == customer_id`), or
* An administrator (role `'admin'` present in `USER_ROLES[current_user_id]`).

If the check fails, the function returns the string `'Unauthorized'`.  If
authorized but no invoice exists for the requested customer, it returns
`None`.

"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would be loaded from a database.
# --------------------------------------------------------------------------- #

USER_ROLES: dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: dict[int, str] = {
    2: "Invoice for user 2 – amount $100",
    3: "Invoice for user 3 – amount $200",
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def download_invoice(current_user_id: int, customer_id: int) -> _t.Optional[str]:
    """
    Return the invoice data for *customer_id* if the request is authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    customer_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Optional[str]
        Invoice data if authorized, otherwise the string `'Unauthorized'`.
        If the invoice does not exist for the customer, returns ``None``.

    Notes
    -----
    * This function performs a strict authorization check to mitigate CWE‑862.
      It does **not** rely on any external authentication context; the caller
      must provide a trustworthy `current_user_id`.
    * The function is deliberately simple and stateless; it does not modify
      any global state or write to disk.
    """
    # Fetch the roles for the requesting user; default to empty list if unknown
    requester_roles: list[str] = USER_ROLES.get(current_user_id, [])

    # Authorization logic:
    is_owner: bool = current_user_id == customer_id
    is_admin: bool = "admin" in requester_roles

    if not (is_owner or is_admin):
        return "Unauthorized"

    # At this point the caller is authorized; fetch the invoice if present
    return INVOICES.get(customer_id)


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(download_invoice(2, 2))  # Owner: should return invoice
    print(download_invoice(1, 3))  # Admin: should return invoice for user 3
    print(download_invoice(2, 3))  # Unauthorized: not owner or admin