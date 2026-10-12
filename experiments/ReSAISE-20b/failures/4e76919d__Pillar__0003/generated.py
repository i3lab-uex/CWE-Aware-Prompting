from typing import Any, Dict

# Sample data structures (replace with actual data in production)
USER_ROLES: Dict[int, str] = {
    # user_id: role
    1: "admin",
    2: "customer",
    3: "customer",
}
INVOICES: Dict[int, Any] = {
    # user_id: invoice data (could be a dict, string, bytes, etc.)
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 180.5},
}


def get_invoice(requester_id: int, client_id: int) -> Any:
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
    Any
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role == 'admin') can access any invoice.
    * Customers can only access their own invoice.
    """
    # Basic input validation
    if not isinstance(requester_id, int) or not isinstance(client_id, int):
        return "Unauthorized"

    # Determine requester role
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Authorization logic
    authorized = False
    if requester_role == "admin":
        authorized = True
    elif requester_id == client_id and requester_role == "customer":
        authorized = True

    if not authorized:
        return "Unauthorized"

    # Retrieve invoice data
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    return invoice