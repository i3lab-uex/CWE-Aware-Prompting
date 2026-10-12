import copy

# Sample database of accounts (normally this would be a secure, persistent store)
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_003", "balance": 1500.00},
}

# Roles that have elevated privileges
ADMIN_ROLES = {"bank_admin", "customer_service"}


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts with proper authorization and validation.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number from which funds will be debited.
    account_to : str
        Account number to which funds will be credited.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating the transaction was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid inputs such as non-existent accounts, negative amounts,
        or insufficient funds.
    """
    # Validate amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    acct_from = ACCOUNTS_DB.get(account_from)
    acct_to = ACCOUNTS_DB.get(account_to)

    if not acct_from or not acct_to:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization logic
    # 1. Admin roles can transfer any accounts.
    # 2. Non-admins must own both source and destination accounts to transfer.
    if u_role not in ADMIN_ROLES:
        # Non-admin must own the source account
        if acct_from["owner_id"] != u_identifier:
            raise PermissionError("User does not own the source account.")
        # Non-admin must also own the destination account
        if acct_to["owner_id"] != u_identifier:
            raise PermissionError("User does not own the destination account.")

    # Check sufficient funds
    if acct_from["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform the transfer atomically (simple simulation)
    # In real systems, this would be a database transaction.
    acct_from["balance"] -= transfer_amount
    acct_to["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {account_from} to "
        f"{account_to} completed successfully."
    )