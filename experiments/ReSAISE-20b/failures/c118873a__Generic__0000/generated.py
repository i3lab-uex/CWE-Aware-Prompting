# Example data structures (replace with actual application data)
USER_ROLES = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.0, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 175.5, "items": ["thingamajig"]},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Return the invoice data for `invoice_owner_id` if the logged in user is
    authorized to view it.

    Parameters
    ----------
    logged_in_user_id : int
        ID of the user attempting to access the invoice.
    invoice_owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice details if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID does not exist in USER_ROLES or the invoice does not exist.
    """
    # Validate that both user IDs exist
    if logged_in_user_id not in USER_ROLES:
        raise KeyError(f"User ID {logged_in_user_id} not found.")
    if invoice_owner_id not in INVOICES:
        raise KeyError(f"Invoice for user ID {invoice_owner_id} not found.")

    # Check role
    roles = USER_ROLES[logged_in_user_id]
    if "admin" in roles or logged_in_user_id == invoice_owner_id:
        return INVOICES[invoice_owner_id]

    return "Unauthorized"