import typing

# Example data structures (replace with real data in production)
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: dict[int, typing.Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.00},
    3: {"invoice_id": "INV-002", "amount": 75.50},
    # ...
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> typing.Any:
    """
    Retrieve an invoice for a specific user if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `requestor_id` or `account_holder_id` does not exist in the system.
    """
    # Validate existence of both users
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor ID {requestor_id} does not exist.")
    if account_holder_id not in USER_ROLES:
        raise KeyError(f"Account holder ID {account_holder_id} does not exist.")

    # Authorization check
    is_admin = USER_ROLES[requestor_id] == "admin"
    is_owner = requestor_id == account_holder_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # Retrieve invoice
    try:
        return INVOICES[account_holder_id]
    except KeyError:
        # No invoice exists for this user
        return None