from typing import Dict, Any

# Example data structures – replace with actual data in production.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 175.50},
}

def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for a given client if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string 'Unauthorized'.
    """
    # Validate that requester exists
    if requester_id not in USER_ROLES:
        return "Unauthorized"

    # Validate that client exists
    if client_id not in INVOICES:
        return "Unauthorized"

    requester_role = USER_ROLES[requester_id]

    # Authorization check:
    #   - Admins can access any invoice.
    #   - Regular customers can only access their own invoice.
    if requester_role == "admin" or requester_id == client_id:
        return INVOICES[client_id]

    # If none of the above, deny access
    return "Unauthorized"