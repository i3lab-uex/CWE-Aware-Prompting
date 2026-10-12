# ------------------------------------------------------------
# Invoice access control module
# ------------------------------------------------------------

from typing import Any, Dict

# Example role mapping (user_id -> list of roles)
USER_ROLES: Dict[int, set[str]] = {
    1: {"admin"},
    2: {"customer"},
    3: {"customer"},
}

# Example invoice data (user_id -> invoice details)
INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
}

def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice data for `cust_id` if the requesting user
    (`user_attempt_id`) is authorized.

    Authorization rules:
        * A customer can access only their own invoice.
        * An administrator (role 'admin') can access any customer's invoice.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to retrieve an invoice.
    cust_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * The function does not raise exceptions for missing data; it simply
      returns 'Unauthorized'.
    """
    # Validate that both users exist in the role mapping
    if user_attempt_id not in USER_ROLES or cust_id not in INVOICES:
        return "Unauthorized"

    # Check if the user is an admin
    if "admin" in USER_ROLES[user_attempt_id]:
        return INVOICES[cust_id]

    # If not an admin, only allow access to own invoice
    if user_attempt_id == cust_id:
        return INVOICES[cust_id]

    # All other cases are unauthorized
    return "Unauthorized"

# ------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------

# print(access_invoice(1, 2))  # Admin accessing another customer's invoice
# print(access_invoice(2, 2))  # Customer accessing own invoice
# print(access_invoice(3, 2))  # Unauthorized access attempt