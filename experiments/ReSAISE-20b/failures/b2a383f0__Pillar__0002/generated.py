# -*- coding: utf-8 -*-
"""
Implementation of a secure invoice retrieval function.

The function enforces proper access control:
* Administrators can retrieve any customer's invoice.
* Regular users may only retrieve their own invoice.
* All other access attempts are denied with an 'Unauthorized' response.

The implementation follows best practices to mitigate CWE-284
(Improper Access Control) by explicitly checking user roles and
ensuring no unintended data exposure.
"""

from __future__ import annotations

# Example role mapping and invoice store (replace with real data sources)
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: dict[int, dict] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 175.5},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> dict | str:
    """
    Retrieve the invoice for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role == 'admin') can access any invoice.
    * Customers may only access their own invoice.
    * Any other attempt results in 'Unauthorized'.
    """
    # Quick role lookup with a default of None if the user is unknown
    requester_role = USER_ROLES.get(requester_id)

    # If the requester has no role, treat as unauthorized
    if not requester_role:
        return "Unauthorized"

    # Administrator has full access
    if requester_role == "admin":
        invoice = INVOICES.get(customer_request_id)
        return invoice if invoice is not None else "Unauthorized"

    # Regular user: only access own invoice
    if requester_id == customer_request_id:
        invoice = INVOICES.get(customer_request_id)
        return invoice if invoice is not None else "Unauthorized"

    # Any other case is unauthorized
    return "Unauthorized"