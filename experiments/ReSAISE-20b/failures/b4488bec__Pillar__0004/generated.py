#!/usr/bin/env python3
"""
Secure invoice retrieval module.

This module defines a single function, `fetch_invoice`, which enforces
role-based access control before returning invoice data.  The function
prevents CWE-284 (Improper Access Control) by ensuring that only the
invoice owner or an administrator can access a given invoice.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

# Example user roles: 1 = admin, 2 = customer, 3 = guest
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "guest",
}

# Example invoice data keyed by user_id
INVOICES: dict[int, str] = {
    2: "Invoice for user 2: $100",
    4: "Invoice for user 4: $250",
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class UnauthorizedError(RuntimeError):
    """Raised when a user attempts to access an invoice they are not authorized for."""
    pass

class InvoiceNotFoundError(RuntimeError):
    """Raised when the requested invoice does not exist."""
    pass

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def fetch_invoice(user_id: int, customer: int) -> str:
    """
    Return the invoice data for a given customer if the requesting user is
    authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    str
        The invoice data if access is permitted.

    Raises
    ------
    UnauthorizedError
        If the user does not have permission to view the invoice.
    InvoiceNotFoundError
        If no invoice exists for the specified customer.
    ValueError
        If either user_id or customer is not a positive integer.

    Notes
    -----
    - Only the invoice owner or an administrator may retrieve the invoice.
    - The function performs input validation and role checks to mitigate
      CWE-284 (Improper Access Control).
    """
    # Validate input types and values
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"user_id must be a positive integer, got {user_id!r}")
    if not isinstance(customer, int) or customer <= 0:
        raise ValueError(f"customer must be a positive integer, got {customer!r}")

    # Retrieve roles; default to 'guest' if user not known
    requester_role = USER_ROLES.get(user_id, "guest")
    # Debug: log roles (in production replace with proper logging)
    # print(f"Requester {user_id} role: {requester_role}")

    # Authorization logic
    if requester_role != "admin" and user_id != customer:
        raise UnauthorizedError("User is not authorized to access this invoice")

    # Retrieve the invoice
    try:
        invoice = INVOICES[customer]
    except KeyError as exc:
        raise InvoiceNotFoundError(f"No invoice found for customer {customer}") from exc

    return invoice

# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test cases to illustrate functionality
    tests = [
        (1, 2),   # admin fetching another user's invoice
        (2, 2),   # owner fetching own invoice
        (3, 2),   # guest attempting to fetch
        (4, 5),   # owner with no invoice
    ]

    for uid, cust in tests:
        try:
            print(f"User {uid} requesting invoice of {cust}:")
            print(fetch_invoice(uid, cust))
        except Exception as e:
            print(f"  -> {type(e).__name__}: {e}")
        print("-" * 40)