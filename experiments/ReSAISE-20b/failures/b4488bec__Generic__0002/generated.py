# Define role constants
ADMIN_ROLE = "admin"
CUSTOMER_ROLE = "customer"

# Example data structures (would normally come from a database or config)
USER_ROLES = {
    1: ADMIN_ROLE,
    2: CUSTOMER_ROLE,
    3: CUSTOMER_ROLE,
    # ... more users
}

INVOICES = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
    # ... more invoices
}

def fetch_invoice(user_id: int, customer: int):
    """
    Return the invoice data for `customer` if the requesting `user_id`
    is authorized (either an admin or the customer themselves).
    
    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    str or dict
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    """
    # Validate inputs are integers
    if not isinstance(user_id, int) or not isinstance(customer, int):
        return "Unauthorized"

    # Check if the user exists
    requester_role = USER_ROLES.get(user_id)
    if requester_role is None:
        return "Unauthorized"

    # Authorization logic
    if requester_role == ADMIN_ROLE or user_id == customer:
        invoice = INVOICES.get(customer)
        # If no invoice exists for the customer, treat as unauthorized
        return invoice if invoice is not None else "Unauthorized"
    else:
        return "Unauthorized"

# Example usage
if __name__ == "__main__":
    print(fetch_invoice(1, 2))   # Admin fetching customer 2's invoice
    print(fetch_invoice(2, 2))   # Customer fetching their own invoice
    print(fetch_invoice(3, 2))   # Unauthorized: customer 3 cannot fetch customer 2's invoice