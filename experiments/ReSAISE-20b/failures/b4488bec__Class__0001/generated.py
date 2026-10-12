# ------------------------------------------------------------------
# Invoice retrieval module
# ------------------------------------------------------------------

# Example role definitions. In a real application these would be loaded from a database or config.
USER_ROLES = {
    1: "admin",      # Administrator
    2: "customer",   # Regular customer
    3: "customer",
    4: "admin",
}

# Example invoice data store. Each user_id maps to their invoice content.
INVOICES = {
    2: "Invoice for Customer 2: $150",
    3: "Invoice for Customer 3: $200",
}

def fetch_invoice(user_id: int, customer: int) -> str:
    """
    Return the invoice for *customer* if the requesting *user_id* is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    str
        The invoice text if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If the requested customer's invoice does not exist.
    """
    # 1. Verify that the user exists in the role mapping
    if user_id not in USER_ROLES:
        return "Unauthorized"

    # 2. Check authorization
    role = USER_ROLES[user_id]
    if user_id != customer and role.lower() != "admin":
        return "Unauthorized"

    # 3. Retrieve the invoice
    try:
        return INVOICES[customer]
    except KeyError:
        # Invoice not found; raise for clarity (could also return a message)
        raise KeyError(f"Invoice for customer {customer} not found.")


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# print(fetch_invoice(1, 2))  # Admin fetching another customer's invoice
# print(fetch_invoice(2, 2))  # Customer fetching own invoice
# print(fetch_invoice(3, 2))  # Unauthorized access attempt