# access_invoice.py

# Sample role and invoice dictionaries for illustration.
# In real usage, these would be provided by the application context.
USER_ROLES = {
    1: ['admin'],
    2: ['customer'],
    3: ['customer'],
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 175.5},
}

def access_invoice(user_attempt_id: int, cust_id: int):
    """
    Return the invoice for `cust_id` if the requesting user (`user_attempt_id`)
    is either an administrator or the owner of the invoice.
    
    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer ID whose invoice is requested.

    Returns
    -------
    dict | str
        The invoice dictionary if access is permitted, otherwise the string 'Unauthorized'.
    """
    # Verify that both users exist in the system
    if user_attempt_id not in USER_ROLES or cust_id not in INVOICES:
        return "Unauthorized"

    # Determine if the requesting user is an admin
    user_roles = USER_ROLES.get(user_attempt_id, [])
    is_admin = 'admin' in [role.lower() for role in user_roles]

    # Allow access if the user is an admin or accessing their own invoice
    if is_admin or user_attempt_id == cust_id:
        return INVOICES[cust_id]

    # Default to unauthorized
    return "Unauthorized"