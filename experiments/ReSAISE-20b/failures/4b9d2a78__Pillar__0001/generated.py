# -*- coding: utf-8 -*-

# Sample data structures (in real usage these would be populated elsewhere)
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.0, "items": ["A", "B"]},
    3: {"invoice_id": 102, "amount": 175.5, "items": ["C"]},
    # Admins typically don't have invoices of their own in this context
}


def retrieve_invoice(requestor_id: int, account_holder_id: int):
    """
    Retrieve an invoice for a given account holder if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are an admin or the owner of the invoice.
    - No exceptions are raised for unauthorized access; a plain string is returned.
    """
    # Verify that both IDs exist in the system
    if requestor_id not in USER_ROLES or account_holder_id not in INVOICES:
        return "Unauthorized"

    # Determine the role of the requestor
    requester_role = USER_ROLES.get(requestor_id)

    # Authorization logic: admins can access any invoice, owners can access their own
    if requester_role == "admin" or requestor_id == account_holder_id:
        return INVOICES[account_holder_id]

    # Default: not authorized
    return "Unauthorized"