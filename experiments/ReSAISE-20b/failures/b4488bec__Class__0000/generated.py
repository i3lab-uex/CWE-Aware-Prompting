from typing import Dict, Any

# Example role mapping and invoice storage. In a real application these would
# come from a database or external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 120.50, "date": "2024-07-01"},
    3: {"invoice_id": "INV-002", "amount": 75.00,  "date": "2024-07-02"},
}

def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Return the invoice data for a given customer if the requesting user is
    authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice data if the user is authorized, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are the customer themselves or if their
      role is 'admin'.
    - This function performs a strict equality check on the user roles to
      avoid accidental privilege escalation.
    """
    # Check if the customer exists in the invoice store
    if customer not in INVOICES:
        return "Unauthorized"

    # Retrieve the role of the requesting user, defaulting to None
    role = USER_ROLES.get(user_id)

    # Authorization logic:
    # 1. The user can access their own invoice.
    # 2. Admins can access any customer's invoice.
    if user_id == customer or role == "admin":
        return INVOICES[customer]

    # If none of the conditions are met, deny access.
    return "Unauthorized"