# -*- coding: utf-8 -*-
"""
Secure invoice retrieval module.

This module defines a single function, `retrieve_invoice`, that enforces
proper access control when returning invoice data.  The function ensures
that only the owner of an invoice or a user with administrative privileges
can access the data.  Any attempt by an unauthorized user results in the
string `'Unauthorized'`.

The module follows best practices for handling potential security issues,
such as:
- Using explicit membership checks rather than implicit truthiness.
- Avoiding accidental leakage of sensitive data by returning a safe
  placeholder string for unauthorized access.
"""

from typing import Dict, Any

# Example data structures. In a real application these would be populated
# from a database or external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "support",  # non-admin role
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 125.50, "status": "unpaid"},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve the invoice belonging to `customer_request_id` if and only if
    `requester_id` is either the same user or an administrator.

    Parameters:
        requester_id (int): The ID of the user attempting to access the invoice.
        customer_request_id (int): The ID of the customer whose invoice is requested.

    Returns:
        dict: Invoice data if access is authorized.
        str: 'Unauthorized' if the requester lacks permission.

    Raises:
        KeyError: If either user ID does not exist in USER_ROLES or the
                  customer has no invoice entry.
    """
    # Validate that both user IDs exist in the role mapping
    if requester_id not in USER_ROLES:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if customer_request_id not in USER_ROLES:
        raise KeyError(f"Customer ID {customer_request_id} does not exist.")

    # Determine if the requester is an admin
    is_admin = USER_ROLES[requester_id].lower() == "admin"

    # Access control: allow if requester is the owner or an admin
    if requester_id == customer_request_id or is_admin:
        # Ensure the invoice exists for the customer
        if customer_request_id not in INVOICES:
            raise KeyError(f"No invoice found for customer ID {customer_request_id}.")
        return INVOICES[customer_request_id]

    # Unauthorized access attempt
    return "Unauthorized"