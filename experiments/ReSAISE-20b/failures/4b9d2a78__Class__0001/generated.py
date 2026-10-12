# -*- coding: utf-8 -*-

"""
Invoice retrieval module.

This module implements a secure invoice retrieval function that enforces
role‑based access control. It protects against CWE-862 by ensuring that
only authorized users can access invoice data.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database or
# external service. They are defined here for the sake of completeness.
# --------------------------------------------------------------------------- #

# Mapping of user_id -> role. Roles are strings: "admin" or "customer".
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "admin",
}

# Mapping of user_id -> invoice data (could be a dict, JSON string,
# PDF bytes, etc.). Here we use simple strings for illustration.
INVOICES = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def retrieve_invoice(requestor_id: int, account_holder_id: int) -> str:
    """
    Retrieve the invoice for a given customer if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    str
        The invoice data if access is permitted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * An administrator (role == "admin") may access any invoice.
    * A customer may only access their own invoice.
    * If either user ID is unknown, or the invoice does not exist,
      the function returns 'Unauthorized' to avoid leaking information.
    """
    # Validate that both users exist in the role mapping
    requestor_role = USER_ROLES.get(requestor_id)
    if requestor_role is None:
        # Unknown requester – deny access
        return "Unauthorized"

    # Authorization logic
    if requestor_role == "admin":
        # Admins can access any invoice
        pass
    elif requestor_role == "customer":
        # Customers may only access their own invoice
        if requestor_id != account_holder_id:
            return "Unauthorized"
    else:
        # Undefined role – deny access
        return "Unauthorized"

    # Fetch the invoice data; if missing, treat as unauthorized
    invoice = INVOICES.get(account_holder_id)
    if invoice is None:
        return "Unauthorized"

    # All checks passed – return the invoice
    return invoice

# --------------------------------------------------------------------------- #
# Example usage (commented out to keep the module clean)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(retrieve_invoice(1, 2))  # Admin accessing user 2's invoice
#     print(retrieve_invoice(2, 2))  # User accessing own invoice
#     print(retrieve_invoice(2, 3))  # User trying to access another's invoice
#     print(retrieve_invoice(5, 2))  # Unknown requester