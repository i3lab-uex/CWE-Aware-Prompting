from typing import Dict, Any

# Example role mapping: 1 = admin, others are regular users
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... add more users as needed
}

# Example invoice data per user
INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.00},
    3: {"invoice_id": 102, "amount": 175.50},
    # ... add more invoices as needed
}


def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Return the invoice for `cust_id` if the requesting user (`user_attempt_id`)
    is authorized to view it.  Administrators can access any invoice, while
    regular users may only view their own.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access an invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice dictionary if access is permitted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    This function performs a strict authorization check to mitigate CWE-862
    (Missing Authorization).  It verifies the role of the requesting user and
    ensures that only admins or the owner can retrieve an invoice.
    """
    # Validate user existence
    if user_attempt_id not in USER_ROLES:
        return "Unauthorized"

    # Fetch role of the attempting user
    role = USER_ROLES[user_attempt_id]

    # Authorization logic: admins or owner can access
    if role == "admin" or user_attempt_id == cust_id:
        # Ensure the requested invoice exists
        return INVOICES.get(cust_id, "Unauthorized")
    else:
        return "Unauthorized"