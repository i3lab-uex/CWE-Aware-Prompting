from typing import Dict, Any

# Example data – in a real application these would come from a database or other storage
USER_ROLES: Dict[int, str] = {
    1: "ADMIN",
    2: "CUSTOMER",
    3: "CUSTOMER",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 125.50},
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    dict | str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in USER_ROLES or INVOICES.
    """
    # Verify that both users exist
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor ID {requestor_id} does not exist.")
    if account_holder_id not in INVOICES:
        raise KeyError(f"Account holder ID {account_holder_id} does not have an invoice.")

    role = USER_ROLES[requestor_id]

    # Access control: admins can access any invoice, customers only their own
    if role == "ADMIN" or requestor_id == account_holder_id:
        return INVOICES[account_holder_id]

    # If we reach here, the user is not authorized
    return "Unauthorized"