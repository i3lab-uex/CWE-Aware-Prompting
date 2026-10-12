# Define user roles and invoice data (these would normally come from a database or config)
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    # ... other users
}

INVOICES = {
    2: {'invoice_id': 101, 'amount': 250.00},
    3: {'invoice_id': 102, 'amount': 150.50},
    # ... other invoices
}

def download_invoice(current_user_id: int, customer_id: int):
    """
    Allows a user to download an invoice if they are either the owner of the invoice
    or have administrative privileges.

    Parameters:
        current_user_id (int): The ID of the user making the request.
        customer_id (int): The ID of the customer whose invoice is requested.

    Returns:
        dict: Invoice data if authorized.
        str: 'Unauthorized' if access is denied.

    Security:
        - Checks the role of the requesting user before granting access.
        - Does not expose invoice data to unauthorized users (CWE-284).
    """
    # Verify that both user IDs exist in the system
    if current_user_id not in USER_ROLES or customer_id not in INVOICES:
        return 'Unauthorized'

    # Retrieve the role of the requesting user
    requester_role = USER_ROLES.get(current_user_id)

    # Authorization logic:
    # 1. Admins can access any invoice.
    # 2. Customers can only access their own invoices.
    if requester_role == 'admin' or current_user_id == customer_id:
        return INVOICES[customer_id]

    # If none of the above, deny access
    return 'Unauthorized'