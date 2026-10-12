# User roles: mapping of user_id to role string ('admin' or 'customer')
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

# Invoices: mapping of user_id to invoice data (could be any serializable type)
INVOICES = {
    2: {"invoice_id": "INV-001", "amount": 250.00, "date": "2024-07-01"},
    3: {"invoice_id": "INV-002", "amount": 125.50, "date": "2024-07-02"},
}

def get_invoice(requester_id: int, client_id: int):
    """
    Return the invoice data for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either requester_id or client_id is not present in USER_ROLES.
    """
    # Ensure both users exist
    if requester_id not in USER_ROLES or client_id not in USER_ROLES:
        raise KeyError("Requester or client does not exist")

    # Authorization check
    requester_role = USER_ROLES[requester_id]
    if requester_id != client_id and requester_role.lower() != "admin":
        return "Unauthorized"

    # Retrieve invoice
    try:
        invoice = INVOICES[client_id]
    except KeyError:
        return "Unauthorized"

    return invoice