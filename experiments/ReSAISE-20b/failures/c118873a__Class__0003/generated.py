# -*- coding: utf-8 -*-

# Sample data structures (to be replaced with actual implementations)
USER_ROLES = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

INVOICES = {
    2: "Invoice for user 2: $100",
    3: "Invoice for user 3: $200",
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Return the invoice details if access is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        ID of the user attempting to retrieve an invoice.
    invoice_owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    str
        Invoice data if access is granted, otherwise 'Unauthorized' or
        'Invoice Not Found'.

    Raises
    ------
    KeyError
        If the logged-in user ID does not exist in USER_ROLES.
    """
    # 1. Ensure the requesting user exists
    if logged_in_user_id not in USER_ROLES:
        raise KeyError(f"User ID {logged_in_user_id} not found in USER_ROLES")

    # 2. Authorization check
    user_roles = USER_ROLES[logged_in_user_id]
    is_admin = "admin" in user_roles
    is_owner = logged_in_user_id == invoice_owner_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # 3. Retrieve invoice
    invoice = INVOICES.get(invoice_owner_id)
    if invoice is None:
        return "Invoice Not Found"

    return invoice