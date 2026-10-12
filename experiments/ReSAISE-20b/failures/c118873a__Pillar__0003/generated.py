# -*- coding: utf-8 -*-

# Sample role and invoice data structures.
# In a real application these would be retrieved from a database or
# another secure storage mechanism.

USER_ROLES = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 120.00, "currency": "USD"},
    3: {"invoice_id": "INV-002", "amount": 250.00, "currency": "USD"},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer who owns the invoice.

    Returns
    -------
    dict | str
        The invoice data if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Only users with role 'admin' or the owner of the invoice may access it.
    - The function performs strict membership checks to mitigate CWE-284
      (Improper Access Control) by ensuring no implicit data leakage.
    """
    # Verify that the logged-in user exists
    if logged_in_user_id not in USER_ROLES:
        return "Unauthorized"

    # Determine whether the user is an administrator
    roles = USER_ROLES.get(logged_in_user_id, [])
    is_admin = "admin" in roles

    # Grant access if the user is an admin or owns the invoice
    authorized = is_admin or (logged_in_user_id == invoice_owner_id)

    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice; if it does not exist, do not reveal that
    # information to an unauthorized user.
    invoice = INVOICES.get(invoice_owner_id)
    if invoice is None:
        # The invoice might not exist or could be in a different state.
        # Returning a generic message avoids leaking information.
        return "Unauthorized"

    return invoice