# SPDX-License-Identifier: MIT
"""
A minimal, secure implementation of an invoice retrieval function.
The function checks that the requesting user is either:
    • An administrator (role contains 'admin'), or
    • The same user whose invoice is being requested.
If the check fails, it returns the string 'Unauthorized'.
"""

from typing import Any, Dict

# Example role and invoice data; in a real system these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 100.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve an invoice for a specific customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to retrieve an invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in the role or invoice dictionaries.
    """
    # Validate existence of users
    if requester_id not in USER_ROLES:
        raise KeyError(f"Requester ID {requester_id} not found.")
    if customer_request_id not in INVOICES:
        raise KeyError(f"Customer ID {customer_request_id} has no invoice.")

    requester_role = USER_ROLES[requester_id].lower()

    # Authorization logic
    if requester_role == "admin" or requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    return "Unauthorized"