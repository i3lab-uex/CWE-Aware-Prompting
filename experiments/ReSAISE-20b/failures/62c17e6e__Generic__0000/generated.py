# ──────────────────────────────────────────────────────────────
#  Invoice Access Control – fetch_invoice implementation
# ──────────────────────────────────────────────────────────────

from typing import Dict, Any

# Example role mapping – replace with real data in production
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

# Example invoice mapping – replace with real data in production
INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
}

def fetch_invoice(req_user_id: int, target_cust_id: int) -> Any:
    """
    Retrieve the invoice for `target_cust_id` if `req_user_id` is authorized.

    Args:
        req_user_id (int): ID of the user making the request.
        target_cust_id (int): ID of the customer whose invoice is requested.

    Returns:
        dict: The invoice data if access is permitted.
        str: 'Unauthorized' if the user lacks permission.

    Raises:
        KeyError: If either `req_user_id` or `target_cust_id` is not found in the
                  respective dictionaries.
    """
    # Validate that both users exist
    if req_user_id not in USER_ROLES:
        raise KeyError(f"Requesting user ID {req_user_id} not found.")
    if target_cust_id not in INVOICES:
        raise KeyError(f"Target customer ID {target_cust_id} has no invoice.")

    # Determine the role of the requesting user
    requester_role = USER_ROLES[req_user_id]

    # Authorization logic:
    #  - Admins can access any invoice.
    #  - Customers can only access their own invoice.
    if requester_role == "admin" or req_user_id == target_cust_id:
        return INVOICES[target_cust_id]

    # All other cases are unauthorized
    return "Unauthorized"