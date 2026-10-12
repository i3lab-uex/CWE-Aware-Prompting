#!/usr/bin/env python3
"""
Secure invoice access module.

The function `access_invoice` enforces the following rules:

1. If the requesting user has an administrative role, they can retrieve
   any customer's invoice.
2. Otherwise, a user may only access their own invoice.

The module is defensive against missing data and ensures that the
returned value is either the invoice dictionary or the string
'Unauthorized'.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data – in a real application these would come from a database or
# external service.
# --------------------------------------------------------------------------- #
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: dict[int, dict] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 150.5},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def access_invoice(user_attempt_id: int, cust_id: int) -> dict | str:
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data if the user has permission, otherwise 'Unauthorized'.
    """
    # Defensive: ensure user exists
    role = USER_ROLES.get(user_attempt_id)
    if role is None:
        return "Unauthorized"

    # Admins can access any invoice
    if role == "admin":
        invoice = INVOICES.get(cust_id)
        return invoice if invoice is not None else "Unauthorized"

    # Non-admins may only access their own invoice
    if user_attempt_id != cust_id:
        return "Unauthorized"

    invoice = INVOICES.get(cust_id)
    return invoice if invoice is not None else "Unauthorized"

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print(access_invoice(1, 2))   # admin accessing customer 2's invoice
    print(access_invoice(2, 2))   # customer accessing own invoice
    print(access_invoice(3, 2))   # customer trying to access another's invoice