# ------------------------------------------------------------
# Invoice retrieval module
# ------------------------------------------------------------

from typing import Any, Dict

# Example data structures (these would normally come from a database or config)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES: Dict[int, str] = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Return the invoice data for *account_holder_id* if the *requestor_id*
    is authorized to access it.

    Parameters
    ----------
    requestor_id : int
        The user ID of the person making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    str | dict
        The invoice data for the requested user.
    str
        'Unauthorized' if the requestor does not have permission.

    Raises
    ------
    KeyError
        If either the requestor or account holder does not exist in USER_ROLES.
    """
    # Validate that both users exist
    if requestor_id not in USER_ROLES:
        raise KeyError(f"Requestor ID {requestor_id} not found.")
    if account_holder_id not in USER_ROLES:
        raise KeyError(f"Account holder ID {account_holder_id} not found.")

    # Permission check: admin can access any invoice; customers only their own
    if (
        USER_ROLES[requestor_id] == "admin"
        or requestor_id == account_holder_id
    ):
        # Retrieve the invoice; raise KeyError if not present to signal missing data
        try:
            return INVOICES[account_holder_id]
        except KeyError as e:
            raise KeyError(f"Invoice for user {account_holder_id} not found.") from e
    else:
        return "Unauthorized"