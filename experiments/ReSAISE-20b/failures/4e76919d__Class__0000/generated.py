# Global dictionaries representing user roles and invoices.
# In a real application these would come from a database or external service.
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
    # ... other invoices
}

def get_invoice(requester_id: int, client_id: int):
    """
    Retrieve the invoice for a given client if the requester is authorized.

    Parameters:
        requester_id (int): The user ID of the person making the request.
        client_id (int): The user ID of the customer whose invoice is requested.

    Returns:
        dict: The invoice data if authorized.
        str : 'Unauthorized' if the requester lacks permission or
              the requested invoice does not exist.
    """
    # Basic type checks to guard against malicious input
    if not isinstance(requester_id, int) or not isinstance(client_id, int):
        return "Unauthorized"

    # Retrieve roles; default to None if user not found
    requester_role = USER_ROLES.get(requester_id)
    client_invoice = INVOICES.get(client_id)

    # No invoice exists for the requested client
    if client_invoice is None:
        return "Unauthorized"

    # Authorization logic:
    # 1. Admins can access any invoice
    # 2. Customers can only access their own invoice
    if requester_role == "admin" or requester_id == client_id:
        return client_invoice

    # If none of the conditions met, deny access
    return "Unauthorized"