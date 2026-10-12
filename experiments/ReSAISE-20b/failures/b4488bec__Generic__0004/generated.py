# -*- coding: utf-8 -*-

"""
Invoice fetching utility.

This module defines a single function `fetch_invoice` that checks whether the
requesting user is authorized to download an invoice and returns the relevant
invoice data or an 'Unauthorized' message.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration (normally these would be loaded from a database or config file)
# --------------------------------------------------------------------------- #

# Example mapping of user IDs to their roles.
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

# Example mapping of user IDs to their invoice data.
INVOICES = {
    2: "Invoice for customer 2: $120.00",
    3: "Invoice for customer 3: $85.50",
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def fetch_invoice(user_id: int, customer: int) -> str:
    """
    Retrieve the invoice data for a given customer if the requesting user is
    authorized.

    Parameters:
        user_id (int): ID of the user making the request.
        customer (int): ID of the customer whose invoice is requested.

    Returns:
        str: The invoice data if authorized, otherwise 'Unauthorized'.

    Notes:
        - An admin can download any customer's invoice.
        - A customer can only download their own invoice.
        - If the requested customer does not have an invoice, returns
          'Invoice not found'.
    """
    # Validate input types
    if not isinstance(user_id, int) or not isinstance(customer, int):
        raise TypeError("user_id and customer must be integers")

    # Determine user role
    role = USER_ROLES.get(user_id)

    # Authorization check
    if role == "admin" or user_id == customer:
        invoice = INVOICES.get(customer)
        if invoice is None:
            return "Invoice not found"
        return invoice

    # Unauthorized access
    return "Unauthorized"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
    print(fetch_invoice(2, 3))   # Customer 2 trying to access customer 3's invoice
    print(fetch_invoice(2, 2))   # Customer accessing their own invoice
    print(fetch_invoice(3, 5))   # Non-existent customer invoice