# Access control for customer invoices

USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... add more users as needed
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
    # ... add more invoices as needed
}


def access_invoice(user_attempt_id: int, cust_id: int):
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is permitted; otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - An admin (role == 'admin') can access any customer's invoice.
    """
    # Validate that both users exist
    user_role = USER_ROLES.get(user_attempt_id)
    if user_role is None:
        return "Unauthorized"

    # Check for admin privilege
    if user_role == "admin":
        invoice = INVOICES.get(cust_id)
        return invoice if invoice is not None else "Unauthorized"

    # Non-admin users may only access their own invoice
    if user_attempt_id == cust_id:
        return INVOICES.get(cust_id, "Unauthorized")

    return "Unauthorized"