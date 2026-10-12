# -*- coding: utf-8 -*-

"""
Utility for retrieving invoices with role‑based access control.
"""

from typing import Any, Dict

# Example user roles and invoices. In a real system these would come from a database.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-002", "amount": 150.00, "date": "2024-07-01"},
    3: {"invoice_id": "INV-003", "amount": 200.00, "date": "2024-07-02"},
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Retrieve the invoice for a specific customer if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual requesting the invoice.
    account_holder_id : int
        The user ID of the customer whose invoice is being fetched.

    Returns
    -------
    dict | str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not present in USER_ROLES.
    """
    # Validate that both users exist
    if requestor_id not in USER_ROLES:
        raise ValueError(f"Requestor ID {requestor_id} does not exist.")
    if account_holder_id not in USER_ROLES:
        raise ValueError(f"Account holder ID {account_holder_id} does not exist.")

    # Admins can retrieve any invoice
    if USER_ROLES[requestor_id] == "admin":
        return INVOICES.get(account_holder_id, "No invoice found.")

    # Customers can only retrieve their own invoices
    if requestor_id == account_holder_id:
        return INVOICES.get(account_holder_id, "No invoice found.")

    # All other cases are unauthorized
    return "Unauthorized"