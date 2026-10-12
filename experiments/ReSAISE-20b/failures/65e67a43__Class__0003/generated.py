from typing import Dict, Any

# Example role definitions
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # add more users as needed
}

# Example invoice data store
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 250.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 125.0, "status": "unpaid"},
    # add more invoices as needed
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice for a customer.

    Args:
        requester_id: ID of the user attempting to fetch the invoice.
        owner_id: ID of the customer whose invoice is requested.

    Returns:
        The invoice data if access is authorized, otherwise the string 'Unauthorized'.
    """
    # Verify that both users exist
    if requester_id not in USER_ROLES or owner_id not in INVOICES:
        return "Unauthorized"

    # Authorization check: requester must be the owner or an admin
    requester_role = USER_ROLES.get(requester_id)
    if requester_id != owner_id and requester_role.lower() != "admin":
        return "Unauthorized"

    # Return the requested invoice
    return INVOICES.get(owner_id, "Unauthorized")