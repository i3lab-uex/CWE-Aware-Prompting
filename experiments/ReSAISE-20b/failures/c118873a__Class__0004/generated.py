# -*- coding: utf-8 -*-
"""
Invoice retrieval module.

Author: ChatGPT
"""

from typing import Any, Dict

# Example role mapping and invoice data.
# In a real application these would come from a database or secure storage.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.50, "status": "unpaid"},
}

def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if the caller is authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    This function performs an authorization check to mitigate CWE-862 (Missing Authorization).
    Only the invoice owner or a user with an 'admin' role can access any customer's invoice.
    """
    # Defensive programming: validate inputs
    if not isinstance(logged_in_user_id, int) or not isinstance(invoice_owner_id, int):
        raise TypeError("User IDs must be integers")

    # Retrieve the role of the logged-in user; default to None if not found.
    role = USER_ROLES.get(logged_in_user_id)

    # Authorization logic
    if logged_in_user_id == invoice_owner_id or role == "admin":
        # Attempt to fetch the invoice; return a copy to prevent accidental mutation.
        invoice = INVOICES.get(invoice_owner_id)
        if invoice is None:
            # Invoice does not exist; could raise a more specific exception.
            return "Invoice not found"
        # Return a shallow copy to avoid exposing internal state
        return invoice.copy()
    else:
        return "Unauthorized"