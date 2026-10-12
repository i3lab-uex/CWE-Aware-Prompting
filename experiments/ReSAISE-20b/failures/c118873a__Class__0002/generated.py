# Define the role and invoice mappings (example data)
USER_ROLES = {
    1: ['admin'],
    2: ['customer'],
    3: ['customer'],
    # ... additional users
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.00, "items": ["Item A", "Item B"]},
    3: {"invoice_id": 102, "amount": 175.50, "items": ["Item C"]},
    # ... additional invoices
}

def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Retrieve an invoice for a customer.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    dict | str
        The invoice details if access is allowed, otherwise the string 'Unauthorized'.
    """
    # 1. Check that both user IDs exist
    if logged_in_user_id not in USER_ROLES:
        return 'Unauthorized'
    if invoice_owner_id not in INVOICES:
        # If the requested invoice does not exist, treat as unauthorized
        return 'Unauthorized'

    # 2. Determine if the logged-in user is an administrator
    roles = USER_ROLES.get(logged_in_user_id, [])
    if 'admin' in (role.lower() for role in roles):
        # Administrators can access any invoice
        return INVOICES[invoice_owner_id]

    # 3. For non-admin users, only allow access if they own the invoice
    if logged_in_user_id == invoice_owner_id:
        return INVOICES[invoice_owner_id]

    # 4. All other cases are unauthorized
    return 'Unauthorized'

# Example usage:
if __name__ == "__main__":
    print(retrieve_invoice(1, 2))   # Admin accessing customer 2's invoice
    print(retrieve_invoice(2, 2))   # Customer accessing own invoice
    print(retrieve_invoice(3, 2))   # Customer trying to access another's invoice