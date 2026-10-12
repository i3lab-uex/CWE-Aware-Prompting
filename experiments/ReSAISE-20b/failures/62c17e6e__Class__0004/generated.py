# Define the user roles and invoices for demonstration purposes.
USER_ROLES = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES = {
    1: {"invoice_id": 101, "amount": 250.0},
    2: {"invoice_id": 102, "amount": 125.5},
    3: {"invoice_id": 103, "amount": 300.0},
}


def fetch_invoice(req_user_id: int, target_cust_id: int):
    """
    Retrieve the invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        The ID of the user making the request.
    target_cust_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not present in the system.
    """
    # Validate that both users exist
    if req_user_id not in USER_ROLES:
        raise ValueError(f"Requesting user ID {req_user_id} does not exist.")
    if target_cust_id not in INVOICES:
        raise ValueError(f"Target customer ID {target_cust_id} does not exist.")

    # Check if the requesting user is an administrator
    roles = USER_ROLES.get(req_user_id, [])
    is_admin = any(role.lower() == "admin" for role in roles)

    # Allow access if the user is an admin or requesting their own invoice
    if is_admin or req_user_id == target_cust_id:
        return INVOICES[target_cust_id]

    # Unauthorized access attempt
    return "Unauthorized"