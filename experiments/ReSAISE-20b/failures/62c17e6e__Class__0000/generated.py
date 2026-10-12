# -*- coding: utf-8 -*-

"""
Security‑aware invoice retrieval.

This module defines a single function, `fetch_invoice`, which enforces
strict access control based on user roles.  The function follows the
principle of least privilege: a user can only view their own invoice,
unless they hold an administrative role.

The implementation protects against common authorization pitfalls
(CWE‑862) by performing explicit checks on the caller’s identity and
role before exposing any sensitive data.  It also handles missing or
malformed inputs gracefully.
"""

from typing import Any, Dict

# Example data stores – in a real application these would come from
# a database or external service.
USER_ROLES: Dict[int, str] = {
    1: "customer",
    2: "admin",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    1: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 103, "amount": 180.0, "status": "unpaid"},
}

def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve the invoice for a customer if the requester is authorized.

    Parameters
    ----------
    req_user_id : int
        The user ID of the requester.
    target_cust_id : int
        The customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can view their own invoice.
    - An administrator (role == 'admin') may view any customer's invoice.
    - If the requester or target does not exist, the function returns
      'Unauthorized' to avoid leaking existence information.
    """
    # Validate that both IDs are integers
    if not isinstance(req_user_id, int) or not isinstance(target_cust_id, int):
        return "Unauthorized"

    # Retrieve roles and invoices safely
    requester_role = USER_ROLES.get(req_user_id)
    invoice = INVOICES.get(target_cust_id)

    # Authorization check
    if requester_role == "admin" or req_user_id == target_cust_id:
        return invoice if invoice is not None else "Unauthorized"

    # Default: unauthorized
    return "Unauthorized"


# Example usage (for local testing only)
if __name__ == "__main__":
    print(fetch_invoice(1, 1))   # Should return customer 1's invoice
    print(fetch_invoice(2, 3))   # Admin accessing customer 3's invoice
    print(fetch_invoice(1, 3))   # Unauthorized access attempt