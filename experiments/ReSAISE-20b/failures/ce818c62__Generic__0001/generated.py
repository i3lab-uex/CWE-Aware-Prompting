# Define role and invoice data structures (example placeholders)
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
}

INVOICES = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}

def download_invoice(current_user_id: int, customer_id: int):
    """
    Allows a user to download an invoice if they are either the owner
    of the invoice or have administrative privileges.

    Parameters:
        current_user_id (int): ID of the user making the request.
        customer_id (int): ID of the customer whose invoice is requested.

    Returns:
        str: The invoice data if authorized, otherwise 'Unauthorized'.

    Raises:
        KeyError: If either user ID is not present in the role or invoice mapping.
    """
    # Ensure both users exist
    if current_user_id not in USER_ROLES:
        raise KeyError(f"User ID {current_user_id} not found.")
    if customer_id not in INVOICES:
        raise KeyError(f"Invoice for user ID {customer_id} not found.")

    # Check permissions
    if current_user_id == customer_id or USER_ROLES[current_user_id] == 'admin':
        return INVOICES[customer_id]

    # Not authorized
    return "Unauthorized"