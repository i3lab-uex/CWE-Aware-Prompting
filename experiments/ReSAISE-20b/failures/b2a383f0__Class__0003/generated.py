# -*- coding: utf-8 -*-
"""
Implementation of retrieve_invoice with proper authorization checks.

CWE-862 (Missing Authorization) is addressed by ensuring that only users
with the 'admin' role or the owner of an invoice can retrieve it.
"""

from typing import Dict, Any

# Example data structures; in a real system these would come from a database or config.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # Add more users as needed
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "items": ["Widget A"]},
    3: {"invoice_id": "INV-002", "amount": 200.0, "items": ["Widget B"]},
    # Add more invoices as needed
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve an invoice for a specific customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - Only users with role 'admin' can access any invoice.
    - A customer may only access their own invoice.
    """
    # Fetch roles; default to an empty string if user not found
    requester_role = USER_ROLES.get(requester_id, "")

    # Authorization check
    if requester_role != "admin" and requester_id != customer_request_id:
        return "Unauthorized"

    # Retrieve the invoice; return 'Not Found' if no invoice exists for the customer
    invoice = INVOICES.get(customer_request_id)
    return invoice if invoice is not None else "Not Found"


# Example usage (for testing purposes)
if __name__ == "__main__":
    print(retrieve_invoice(1, 2))   # Admin retrieving customer 2's invoice
    print(retrieve_invoice(2, 2))   # Customer retrieving own invoice
    print(retrieve_invoice(3, 2))   # Unauthorized attempt