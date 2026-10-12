# -*- coding: utf-8 -*-
"""
Utility for secure invoice retrieval.

The module defines a single function `retrieve_invoice` that enforces
access control based on user roles.  Only administrators may view any
customer's invoice; ordinary users may only view their own.
"""

from typing import Any, Dict

# Example data structures (replace with real data in production)
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 375.5},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Return the invoice for `customer_request_id` if the requester is
    authorized.  Administrators can access any invoice; regular users
    may only retrieve their own.

    Parameters:
        requester_id (int): ID of the user making the request.
        customer_request_id (int): ID of the customer whose invoice is requested.

    Returns:
        The invoice data if authorized; otherwise the string 'Unauthorized'.
    """
    # Get roles for requester, defaulting to empty list if not found
    requester_roles = USER_ROLES.get(requester_id, [])

    # Admin check – allow any access
    if "admin" in requester_roles:
        return INVOICES.get(customer_request_id, "Unauthorized")

    # Regular user check – must be accessing own invoice
    if requester_id == customer_request_id:
        return INVOICES.get(requester_id, "Unauthorized")

    # If none of the above, deny access
    return "Unauthorized"