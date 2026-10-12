from typing import Any, Dict

# Example data – in a real system these would come from a database
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "items": ["widget A", "widget B"]},
    3: {"invoice_id": 102, "amount": 150.0, "items": ["widget C"]},
    # ... other invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Return the invoice data for a given customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized' or 'Not found'.
    """
    # Validate that both IDs exist in USER_ROLES
    if user_id not in USER_ROLES or customer not in USER_ROLES:
        return "Unauthorized"

    # Only admins can fetch any invoice; customers may only fetch their own
    if user_id == customer:
        # Customer requesting own invoice – allowed
        pass
    elif USER_ROLES[user_id] == "admin":
        # Admin requesting any invoice – allowed
        pass
    else:
        return "Unauthorized"

    # Retrieve the invoice data
    invoice = INVOICES.get(customer)
    if invoice is None:
        return "Not found"

    # Return a copy to prevent accidental modification
    return dict(invoice)