#!/usr/bin/env python3
"""
Invoice retrieval module.

Provides a single function `get_invoice` that returns the invoice data for a
given customer if and only if the requester is authorized. Authorization rules:

* A user can download their own invoice.
* An administrator (role == "admin") can download any customer's invoice.

If the requester is not authorized or if either user id does not exist, the
function returns the string 'Unauthorized'.
"""

from __future__ import annotations

from typing import Any, Dict


# Sample data structures (these would normally be loaded from a database)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... more users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 175.50, "items": ["thingamajig"]},
    # ... more invoices
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Return the invoice data for `client_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user id of the individual making the request.
    client_id : int
        The user id whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * Authorization is based on USER_ROLES and direct ownership.
    * Missing user ids or invoices are treated as unauthorized to avoid leaking
      information about account existence.
    """
    # Validate that both users exist in the system
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Check ownership or admin privilege
    authorized = requester_id == client_id or requester_role.lower() == "admin"
    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice; missing invoices are also treated as unauthorized
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the global data
    return invoice.copy()


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    print(get_invoice(1, 2))  # Admin fetching customer 2's invoice
    print(get_invoice(2, 2))  # Customer fetching own invoice
    print(get_invoice(3, 2))  # Unauthorized access attempt