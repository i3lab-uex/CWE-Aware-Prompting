# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example role and invoice data. In a real system these would come from a database.
USER_ROLES: Dict[int, str] = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
}

INVOICES: Dict[int, Any] = {
    2: {'invoice_id': 101, 'amount': 250.00, 'items': ['widget', 'gadget']},
    3: {'invoice_id': 102, 'amount': 125.50, 'items': ['widget']},
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for `customer_id` if the requesting user is authorized.
    An admin can download any invoice; a customer can only download their own.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor making the request.
    customer_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - The function performs an explicit authorization check to mitigate CWE-862.
    - It gracefully handles missing user IDs or invoices by treating them as unauthorized.
    """
    # Basic validation of input types
    if not isinstance(current_user_id, int) or not isinstance(customer_id, int):
        return 'Unauthorized'

    # Retrieve roles safely; treat unknown users as non-admin
    current_role = USER_ROLES.get(current_user_id, None)

    # Authorization logic: admin or owner
    if current_role != 'admin' and current_user_id != customer_id:
        return 'Unauthorized'

    # Retrieve the invoice; if not found, treat as unauthorized
    invoice = INVOICES.get(customer_id)
    if invoice is None:
        return 'Unauthorized'

    return invoice