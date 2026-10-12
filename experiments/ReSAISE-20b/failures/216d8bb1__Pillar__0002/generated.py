# Access control for invoice retrieval

# Example data structures (replace with real ones in production)
USER_ROLES = {
    # user_id: role
    1: 'admin',
    2: 'customer',
    3: 'customer',
}

INVOICES = {
    # user_id: invoice data
    2: {"invoice_id": "INV-001", "amount": 100.0, "items": ["A", "B"]},
    3: {"invoice_id": "INV-002", "amount": 200.0, "items": ["C"]},
}


def access_invoice(user_id: int, client_id: int):
    """
    Return the invoice for `client_id` if the requesting user has permission.
    
    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access the invoice.
    client_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Check that both IDs exist
    if user_id not in USER_ROLES:
        return "Unauthorized"
    if client_id not in INVOICES:
        # No invoice exists for this customer; treat as unauthorized
        return "Unauthorized"

    role = USER_ROLES[user_id]

    # Admins can access any invoice
    if role == "admin":
        return INVOICES[client_id]

    # Customers can only access their own invoice
    if role == "customer" and user_id == client_id:
        return INVOICES[client_id]

    # All other cases are unauthorized
    return "Unauthorized"