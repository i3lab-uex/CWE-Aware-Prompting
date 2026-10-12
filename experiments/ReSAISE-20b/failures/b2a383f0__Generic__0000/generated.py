# Define role constants for clarity
ADMIN_ROLE = 'admin'

def retrieve_invoice(requester_id: int, customer_request_id: int):
    """
    Retrieve an invoice for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Verify that both IDs exist in USER_ROLES and INVOICES
    if requester_id not in USER_ROLES or customer_request_id not in INVOICES:
        return 'Unauthorized'

    # Allow admins to access any invoice
    if USER_ROLES.get(requester_id) == ADMIN_ROLE:
        return INVOICES[customer_request_id]

    # Non-admins can only access their own invoice
    if requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    # If none of the above conditions are met, deny access
    return 'Unauthorized'


# Example data structures (to be replaced with real data in production)
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer'
}

INVOICES = {
    2: {'invoice_id': 101, 'amount': 250.00},
    3: {'invoice_id': 102, 'amount': 150.50}
}