# User roles mapping: user_id -> set of role strings (e.g., {"customer"}, {"admin"})
USER_ROLES = {
    1: {"customer"},
    2: {"customer"},
    3: {"admin"},
}

# Invoice storage: user_id -> invoice data (could be any serializable structure)
INVOICES = {
    1: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    2: {"invoice_id": 102, "amount": 175.50, "status": "unpaid"},
}

def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Retrieve an invoice if the logged-in user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    dict or str
        The invoice data if access is allowed, otherwise the string 'Unauthorized'.
    """
    # Ensure both users exist
    if logged_in_user_id not in USER_ROLES or invoice_owner_id not in INVOICES:
        return "Unauthorized"

    # Customer can access only their own invoice
    if logged_in_user_id == invoice_owner_id:
        return INVOICES[invoice_owner_id]

    # Admin can access any invoice
    if "admin" in USER_ROLES[logged_in_user_id]:
        return INVOICES[invoice_owner_id]

    # All other cases are forbidden
    return "Unauthorized"