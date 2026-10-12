# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module defines the `fetch_invoice` function, which allows a user to
download an invoice.  Authorization is enforced based on the `USER_ROLES`
mapping:

* An administrator (`role == "admin"`) can retrieve any invoice.
* A customer (`role == "customer"`) may only retrieve their own invoice.

If the user is not authorized, the function returns the string
"Unauthorized".  If no invoice exists for the requested customer,
`None` is returned.

The implementation avoids common pitfalls such as missing authorization
checks (CWE‑862) and protects against injection attacks by using simple
dictionary lookups rather than dynamic code execution.
"""

from typing import Any, Dict

# Sample data – in a real application these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... more users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 125.00, "items": ["thingamajig"]},
    # ... more invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requesting user is
    authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string "Unauthorized".
        If no invoice exists for the customer, returns None.
    """
    # Validate input types to guard against accidental injection
    if not isinstance(user_id, int) or not isinstance(customer, int):
        raise TypeError("user_id and customer must be integers")

    # Retrieve the role of the requesting user
    requester_role = USER_ROLES.get(user_id)

    # Authorization check – CWE‑862 mitigation
    if requester_role == "admin" or (requester_role == "customer" and user_id == customer):
        # Authorized – fetch the invoice
        return INVOICES.get(customer)
    else:
        # Unauthorized access attempt
        return "Unauthorized"