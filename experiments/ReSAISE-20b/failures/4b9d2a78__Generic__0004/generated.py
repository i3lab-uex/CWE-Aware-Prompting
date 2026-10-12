# -*- coding: utf-8 -*-

"""
Utility for retrieving invoices with role-based access control.

The module defines:
    * USER_ROLES: mapping of user_id -> role string.
      Expected roles are 'customer' and 'admin'.
    * INVOICES: mapping of user_id -> invoice data (any serialisable object).
    * retrieve_invoice(requestor_id, account_holder_id): function that
      returns the invoice data if the requestor is authorized.
"""

from typing import Any, Dict

# Example role mapping (replace with real data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... add more users
}

# Example invoice storage (replace with real data source)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 75.00, "status": "unpaid"},
    # ... add more invoices
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Retrieve the invoice for a given account holder if the requestor has
    sufficient permissions.

    Parameters:
        requestor_id (int): The user ID of the individual making the request.
        account_holder_id (int): The user ID whose invoice is being requested.

    Returns:
        Any: The invoice data associated with `account_holder_id`.

    Raises:
        KeyError: If either the requestor or account holder does not exist in USER_ROLES.
        ValueError: If no invoice exists for the requested account holder.

    Notes:
        - Administrators (role == 'admin') can access any invoice.
        - Customers can only access their own invoices.
    """
    # Validate that both users exist
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor ID {requestor_id} is not a recognized user.")
    if account_holder_id not in USER_ROLES:
        raise KeyError(f"Account holder ID {account_holder_id} is not a recognized user.")

    # Determine the requestor's role
    requestor_role = USER_ROLES[requestor_id]

    # Authorization check
    if requestor_role == "admin":
        authorized = True
    elif requestor_role == "customer" and requestor_id == account_holder_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice
    try:
        invoice = INVOICES[account_holder_id]
    except KeyError as exc:
        raise ValueError(f"No invoice found for account holder ID {account_holder_id}") from exc

    return invoice