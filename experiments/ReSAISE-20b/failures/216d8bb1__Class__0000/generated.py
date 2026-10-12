# Access control for invoice retrieval

# Example role definitions (extend as needed)
ADMIN_ROLE = "admin"

def access_invoice(user_id: int, client_id: int) -> dict | str:
    """
    Retrieve the invoice for `client_id` if the requesting user has
    appropriate permissions.

    Parameters:
        user_id   (int): ID of the requesting user.
        client_id (int): ID of the customer whose invoice is requested.

    Returns:
        dict: Invoice data if authorized.
        str : 'Unauthorized' otherwise.
    """
    # Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(client_id, int):
        return "Unauthorized"

    # Retrieve roles for the requesting user
    user_roles = USER_ROLES.get(user_id, set())

    # Check if the user is an admin or requesting their own invoice
    authorized = (
        ADMIN_ROLE in user_roles
        or user_id == client_id
    )

    if not authorized:
        return "Unauthorized"

    # Retrieve the invoice data; return 'Unauthorized' if missing
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    return invoice