# user_roles.py (example data)
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    # add more users as needed
}

# invoices.py (example data)
INVOICES = {
    2: {'invoice_id': 'INV-001', 'amount': 120.00, 'date': '2024-07-01'},
    3: {'invoice_id': 'INV-002', 'amount': 75.50, 'date': '2024-07-02'},
    # add more invoices as needed
}


def get_invoice(requester_id: int, client_id: int):
    """
    Return the invoice data for `client_id` if the requester is authorized.

    Parameters:
        requester_id (int): The user ID of the individual making the request.
        client_id   (int): The user ID whose invoice is being requested.

    Returns:
        dict or str: Invoice data dictionary if authorized, otherwise 'Unauthorized'.
    """
    # Validate that the requester exists
    role = USER_ROLES.get(requester_id)
    if role is None:
        return 'Unauthorized'

    # Admins can access any invoice
    if role == 'admin':
        return INVOICES.get(client_id, 'Unauthorized')

    # Customers can only access their own invoice
    if role == 'customer' and requester_id == client_id:
        return INVOICES.get(client_id, 'Unauthorized')

    # Any other case is not allowed
    return 'Unauthorized'