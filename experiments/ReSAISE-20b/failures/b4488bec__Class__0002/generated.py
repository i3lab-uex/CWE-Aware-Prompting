from typing import Dict, Any

# Example role definitions: 'admin' or 'customer'
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # add more users as needed
}

# Example invoice storage: mapping user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 150.00, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.00, "status": "unpaid"},
    # add more invoices as needed
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role == 'admin') can access any invoice.
    * Customers can only access their own invoices.
    """
    # Verify that the requesting user exists
    if user_id not in USER_ROLES:
        return "Unauthorized"

    # Determine role of requesting user
    requester_role = USER_ROLES[user_id]

    # Authorization check
    if requester_role != "admin" and user_id != customer:
        return "Unauthorized"

    # Retrieve invoice data; if missing, still return 'Unauthorized' to avoid leaking info
    invoice = INVOICES.get(customer)
    if invoice is None:
        return "Unauthorized"

    return invoice