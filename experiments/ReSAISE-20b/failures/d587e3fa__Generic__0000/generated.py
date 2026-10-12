# -*- coding: utf-8 -*-
"""
Access control helper for invoices.

Author: <your name>
"""

from typing import Dict, Any

# Example data structures. In real use these would come from a database or other storage.
USER_ROLES: Dict[int, str] = {
    1: "customer",
    2: "admin",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    1: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.00, "status": "unpaid"},
}


def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice data for a customer if the user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - An admin (role == 'admin') can access any customer's invoice.
    - If either the user or customer ID does not exist in the system,
      access is denied and 'Unauthorized' is returned.
    """
    # Quick existence check
    if user_attempt_id not in USER_ROLES or cust_id not in INVOICES:
        return "Unauthorized"

    # Allow if user is accessing own invoice
    if user_attempt_id == cust_id:
        return INVOICES[cust_id]

    # Allow admins to access any invoice
    if USER_ROLES.get(user_attempt_id) == "admin":
        return INVOICES[cust_id]

    # All other cases are unauthorized
    return "Unauthorized"


# Example usage (commented out to avoid side effects when imported)
if __name__ == "__main__":
    print(access_invoice(1, 1))   # Own invoice
    print(access_invoice(2, 3))   # Admin accessing another customer's invoice
    print(access_invoice(3, 1))   # Unauthorized attempt