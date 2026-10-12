# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example data structures (in a real system these would come from a database)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... more users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "date": "2024-06-15"},
    3: {"invoice_id": 102, "amount": 125.50, "date": "2024-06-16"},
    # ... more invoices
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Return the invoice data for `account_holder_id` if the requestor is authorized.

    Authorization rules:
      * A user can retrieve their own invoice.
      * An admin (role == "admin") can retrieve any user's invoice.

    Parameters
    ----------
    requestor_id : int
        The user ID of the person making the request.
    account_holder_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * The function performs an explicit authorization check to mitigate CWE-862.
    * It gracefully handles missing users or invoices without leaking information.
    """
    # Check if requestor exists
    role = USER_ROLES.get(requestor_id)
    if role is None:
        return "Unauthorized"

    # Authorization: self or admin
    authorized = requestor_id == account_holder_id or role.lower() == "admin"

    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice; if none exists, still return 'Unauthorized' to avoid leaking info
    invoice = INVOICES.get(account_holder_id)
    if invoice is None:
        return "Unauthorized"

    return invoice