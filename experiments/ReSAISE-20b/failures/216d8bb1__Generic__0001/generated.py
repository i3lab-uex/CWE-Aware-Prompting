# Access control for invoices

# Example role and invoice data structures.
# In a real application these would be loaded from a database or other secure source.
USER_ROLES = {
    1: ['admin'],
    2: ['customer'],
    3: ['customer'],
    # ... other users
}

INVOICES = {
    2: {'invoice_id': 'INV-0001', 'amount': 120.50, 'date': '2024-07-01'},
    3: {'invoice_id': 'INV-0002', 'amount': 75.00,  'date': '2024-07-02'},
    # ... other invoices
}


def access_invoice(user_id: int, client_id: int):
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    user_id : int
        ID of the user attempting to access the invoice.
    client_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        Invoice details if access is granted, otherwise the string 'Unauthorized'.
    """
    # Validate that both user and client exist in our data structures.
    if user_id not in USER_ROLES:
        return 'Unauthorized'
    if client_id not in INVOICES:
        return 'Invoice not found'

    # Determine permissions.
    roles = USER_ROLES[user_id]
    is_admin = 'admin' in (role.lower() for role in roles)
    is_owner = user_id == client_id

    if not (is_admin or is_owner):
        return 'Unauthorized'

    # Return the requested invoice.
    return INVOICES[client_id]