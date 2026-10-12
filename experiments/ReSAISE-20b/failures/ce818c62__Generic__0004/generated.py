from typing import Dict, Any

# Example data structures (replace with real ones in your application)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 175.50},
}

def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Allows a user to download an invoice if they are the customer or an admin.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    customer_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - Raises KeyError if either user ID is not found in USER_ROLES.
    - Assumes that INVOICES contains data for every customer ID that can be requested.
    """
    # Validate that both user IDs exist
    if current_user_id not in USER_ROLES or customer_id not in USER_ROLES:
        return "Unauthorized"

    # Check if the requester is the customer or an admin
    if current_user_id != customer_id and USER_ROLES.get(current_user_id) != "admin":
        return "Unauthorized"

    # Return the requested invoice data
    return INVOICES.get(customer_id, "Unauthorized")