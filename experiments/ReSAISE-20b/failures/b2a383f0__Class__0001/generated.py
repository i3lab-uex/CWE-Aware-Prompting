# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

Author: OpenAI ChatGPT
Date: 2026-07-23
"""

from typing import Dict, Any

# Example data structures – in a real system these would come from a database or
# external service. They are defined here only for demonstration purposes.
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # Add more users as needed
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-002", "amount": 150.00, "status": "paid"},
    3: {"invoice_id": "INV-003", "amount": 200.00, "status": "unpaid"},
    # Add more invoices as needed
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve an invoice for a specific customer.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if the requester is authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * Administrators can access any invoice.
    * Customers may only access their own invoices.
    * This function performs a strict authorization check to prevent
      CWE-862: Missing Authorization.  It does **not** perform any other form of
      authentication or input sanitisation – those are assumed to be handled
      elsewhere in the system.
    """
    # Fetch roles for the requester; if user not found, treat as no roles
    roles = USER_ROLES.get(requester_id, [])

    # Administrator bypass: grant access to any invoice
    if "admin" in roles:
        return INVOICES.get(customer_request_id, "Unauthorized")

    # Customer access: only allow if the requester is requesting their own invoice
    if "customer" in roles and requester_id == customer_request_id:
        return INVOICES.get(customer_request_id, "Unauthorized")

    # Any other scenario is unauthorized
    return "Unauthorized"


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    print(retrieve_invoice(1, 2))  # Admin accessing customer 2's invoice
    print(retrieve_invoice(2, 2))  # Customer accessing own invoice
    print(retrieve_invoice(3, 2))  # Unauthorized attempt