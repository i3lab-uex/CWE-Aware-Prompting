# Mapping of user_id to a list of roles they possess.
USER_ROLES = {
    1: ["customer"],
    2: ["customer"],
    3: ["admin"],
    4: ["customer", "admin"],  # example of a dual role user
}

# Mapping of user_id to their invoice details.
INVOICES = {
    1: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    2: {"invoice_id": 102, "amount": 125.50, "status": "unpaid"},
    # Admins typically don't have their own invoices in this context.
}

def retrieve_invoice(requester_id: int, customer_request_id: int):
    """
    Retrieve an invoice if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access an invoice.
    customer_request_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can always access their own invoice.
    - Users with the 'admin' role may access any invoice.
    - If either user ID is unknown or an invoice does not exist, the function
      returns 'Unauthorized' rather than raising an exception to avoid leaking
      information about user existence.
    """
    # Verify that both requester and customer exist in the role mapping
    if requester_id not in USER_ROLES or customer_request_id not in INVOICES:
        return "Unauthorized"

    # Admin check
    if "admin" in USER_ROLES.get(requester_id, []):
        return INVOICES[customer_request_id]

    # Self-access check
    if requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    # If none of the above, deny access
    return "Unauthorized"