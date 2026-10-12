# access_invoice.py

# Define role constants for clarity
ADMIN_ROLE = "admin"
CUSTOMER_ROLE = "customer"

def access_invoice(user_attempt_id: int, cust_id: int) -> dict | str:
    """
    Return the invoice data for a customer if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if access is permitted, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `user_attempt_id` or `cust_id` is not present in the role mapping.
    """
    # Validate that both user IDs exist
    if user_attempt_id not in USER_ROLES:
        raise KeyError(f"User ID {user_attempt_id} not found.")
    if cust_id not in USER_ROLES:
        raise KeyError(f"Customer ID {cust_id} not found.")

    # Determine if the user is an admin
    is_admin = USER_ROLES[user_attempt_id] == ADMIN_ROLE

    # Authorize: admin or same user
    if is_admin or user_attempt_id == cust_id:
        # Retrieve the invoice; raise KeyError if missing
        return INVOICES[cust_id]
    else:
        return "Unauthorized"