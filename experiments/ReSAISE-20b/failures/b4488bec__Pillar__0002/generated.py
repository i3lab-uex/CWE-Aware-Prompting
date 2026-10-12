# fetch_invoice.py

from typing import Any, Dict

# Example data (in a real system these would come from a database or other secure store)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
    # ... other invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a specific customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if access is permitted, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either `user_id` or `customer` is not present in the role/invoice mappings.
    """
    # Validate that both users exist
    if user_id not in USER_ROLES:
        raise KeyError(f"Requesting user ID {user_id} does not exist.")
    if customer not in INVOICES:
        raise KeyError(f"Invoice for customer ID {customer} does not exist.")

    # Determine if the user is authorized
    requester_role = USER_ROLES[user_id]
    is_admin = requester_role.lower() == "admin"
    is_self = user_id == customer

    if not (is_admin or is_self):
        return "Unauthorized"

    # Return the invoice data
    return INVOICES[customer]