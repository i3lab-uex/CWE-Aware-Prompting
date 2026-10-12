# Dictionary mapping user IDs to a list of roles they possess.
USER_ROLES = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # add more users as needed
}

# Dictionary mapping customer IDs to their invoice data.
INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 150.00, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.00, "status": "unpaid"},
    # add more invoices as needed
}


def fetch_invoice(requester_id: int, owner_id: int):
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to retrieve the invoice.
    owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if the requester is authorized, otherwise 'Unauthorized'.
    """
    # Verify that both users exist
    if requester_id not in USER_ROLES or owner_id not in INVOICES:
        return "Unauthorized"

    # Determine if the requester is an admin
    is_admin = "admin" in USER_ROLES.get(requester_id, [])

    # Allow admins to access any invoice
    if is_admin:
        return INVOICES[owner_id]

    # Allow customers to access only their own invoice
    if requester_id == owner_id:
        return INVOICES[owner_id]

    # All other cases are unauthorized
    return "Unauthorized"