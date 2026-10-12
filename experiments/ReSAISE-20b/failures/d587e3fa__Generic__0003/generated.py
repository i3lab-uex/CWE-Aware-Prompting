#!/usr/bin/env python3
"""
Invoice access control module.

The `access_invoice` function allows a user to retrieve an invoice only if
they are the owner or have an administrative role.  Unauthorized requests
return the string 'Unauthorized'.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would come from a database or an API
# --------------------------------------------------------------------------- #
USER_ROLES: Dict[int, List[str]] = {
    1: ["customer"],
    2: ["customer"],
    3: ["admin"],          # Administrator
    4: ["customer", "vip"],
}

INVOICES: Dict[int, Dict[str, Any]] = {
    1: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    2: {"invoice_id": 102, "amount": 125.5, "status": "unpaid"},
    3: {"invoice_id": 103, "amount": 500.0, "status": "paid"},
    4: {"invoice_id": 104, "amount": 75.0, "status": "paid"},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice data for `cust_id` if the requesting user
    (identified by `user_attempt_id`) is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice dictionary if authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - An admin (role 'admin') can access any invoice.
    - The function does not raise exceptions for normal operation;
      it returns 'Unauthorized' on failure.
    """
    # Quick sanity check: the invoice must exist
    if cust_id not in INVOICES:
        return "Unauthorized"

    # Fetch roles of the attempting user, defaulting to empty list
    roles = USER_ROLES.get(user_attempt_id, [])

    # Authorization logic:
    is_admin = "admin" in roles
    owns_invoice = user_attempt_id == cust_id

    if not (is_admin or owns_invoice):
        return "Unauthorized"

    # Return a deep copy to prevent accidental mutation of the global data
    return copy.deepcopy(INVOICES[cust_id])


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tests = [
        (1, 1),  # own invoice
        (2, 1),  # not own, not admin
        (3, 2),  # admin accessing others' invoice
        (4, 4),  # own invoice with extra role
        (5, 1),  # unknown user attempting to access
    ]

    for uid, cid in tests:
        result = access_invoice(uid, cid)
        print(f"User {uid} accessing customer {cid}: {result}")