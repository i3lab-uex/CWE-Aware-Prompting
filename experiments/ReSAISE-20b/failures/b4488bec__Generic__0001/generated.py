# -*- coding: utf-8 -*-

# Example data structures (these would normally be imported or fetched from a database)
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    # ... other users
}

INVOICES = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
    # ... other invoices
}

def fetch_invoice(user_id: int, customer: int):
    """
    Retrieve an invoice for a given customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    str or dict or None
        The invoice data if the user is authorized; otherwise, the string 'Unauthorized'.
    """
    # Verify that both users exist in the system
    if user_id not in USER_ROLES or customer not in INVOICES:
        return 'Unauthorized'

    # Allow access if the requester is an admin or requesting their own invoice
    role = USER_ROLES.get(user_id)
    if role == 'admin' or user_id == customer:
        return INVOICES.get(customer)

    # If none of the conditions are met, deny access
    return 'Unauthorized'