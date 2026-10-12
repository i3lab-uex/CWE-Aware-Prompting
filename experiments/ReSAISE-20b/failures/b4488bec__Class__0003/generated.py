# -*- coding: utf-8 -*-
"""
Invoice fetching module with role‑based access control.

The module defines a single function `fetch_invoice` that retrieves
invoice data for a given customer.  The function checks the role of the
requesting user and enforces the following policy:

* An administrator (role `'admin'`) may fetch invoices for any user.
* A customer (role `'customer'`) may only fetch their own invoice.

If the requester does not have permission, the function returns the
string `'Unauthorized'`.

This implementation mitigates CWE‑862 (Missing Authorization) by
explicitly validating the requester’s role before granting access.
"""

from typing import Dict, Any

# Example data structures – in a real application these would be
# retrieved from a database or external service.
USER_ROLES: Dict[int, str] = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {'invoice_id': 101, 'amount': 250.00, 'status': 'paid'},
    3: {'invoice_id': 102, 'amount': 150.00, 'status': 'unpaid'},
    # ... other invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a specific customer if the requesting user
    is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * The function performs a minimal check: the requester must exist in
      USER_ROLES and have either the 'admin' role or be requesting their
      own invoice.
    * If the requested customer has no invoice, a `KeyError` will be
      raised.  In production code you might want to catch this and
      return a more user‑friendly message.
    """
    # Validate that the requester exists in our role mapping
    if user_id not in USER_ROLES:
        return 'Unauthorized'

    requester_role = USER_ROLES[user_id]

    # Authorization logic
    if requester_role == 'admin' or (requester_role == 'customer' and user_id == customer):
        # Retrieve invoice data; if missing, raise KeyError
        return INVOICES[customer]
    else:
        return 'Unauthorized'