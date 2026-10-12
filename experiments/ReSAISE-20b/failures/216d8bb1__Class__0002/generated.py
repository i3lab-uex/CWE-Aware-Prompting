# -*- coding: utf-8 -*-
"""
Invoice access control module.

The `access_invoice` function implements role‑based authorization
to protect invoice data.  It ensures that only administrators can
access any invoice, while customers may only retrieve their own.
"""

from __future__ import annotations

# Sample data – in real usage these would come from a database or
# secure storage.  They are kept minimal for clarity.
USER_ROLES: dict[int, str] = {
    # user_id : role
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: dict[int, dict] = {
    # client_id : invoice details
    2: {"invoice_id": 101, "amount": 150.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 200.00, "status": "unpaid"},
}

def access_invoice(user_id: int, client_id: int) -> dict | str:
    """
    Return the invoice details for a given client if the requesting
    user has sufficient privileges.

    Parameters:
        user_id (int): ID of the user attempting access.
        client_id (int): ID of the customer whose invoice is requested.

    Returns:
        dict: Invoice data if authorized.
        str: 'Unauthorized' if access is denied.

    Notes:
        * Administrators (role == "admin") may retrieve any invoice.
        * Customers can only retrieve their own invoice.
        * If the user or client does not exist, access is denied.
    """
    # Fetch role; default to None if user_id unknown
    role = USER_ROLES.get(user_id)

    # No role => unauthorized
    if not role:
        return "Unauthorized"

    # Admins can access any invoice
    if role == "admin":
        return INVOICES.get(client_id, "Unauthorized")

    # Customers may only access their own invoice
    if role == "customer" and user_id == client_id:
        return INVOICES.get(client_id, "Unauthorized")

    # All other cases are denied
    return "Unauthorized"

# Example usage (for testing purposes)
if __name__ == "__main__":
    print(access_invoice(1, 2))  # Admin accessing client 2's invoice
    print(access_invoice(2, 2))  # Client 2 accessing their own invoice
    print(access_invoice(3, 2))  # Client 3 attempting to access client 2's invoice
    print(access_invoice(4, 2))  # Unknown user attempting access