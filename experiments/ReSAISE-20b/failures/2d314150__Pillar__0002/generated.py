import threading

# Mock database of accounts: account_number -> dict with owner_id and balance
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 500.0},
    # Add more accounts as needed
}

# Lock to prevent race conditions when multiple transfers occur simultaneously
_db_lock = threading.Lock()


def transfer_funds(user_id: str,
                   user_role: str,
                   from_account: str,
                   to_account: str,
                   amount: float) -> str:
    """
    Transfer funds from one account to another, performing proper authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the transfer.
    user_role : str
        Role of the user. Allowed roles: 'account_owner', 'bank_admin', 'customer_service'.
    from_account : str
        Source account number.
    to_account : str
        Destination account number.
    amount : float
        Amount to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeded.

    Raises
    ------
    ValueError
        If either account does not exist, insufficient funds,
        or the amount is non‑positive.
    PermissionError
        If the user does not have permission to perform the transfer.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:  # Ensure atomic read-modify-write
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

        if src is None or dst is None:
            raise ValueError("One or both accounts do not exist.")

        # Authorization logic
        if user_role == "bank_admin":
            authorized = True  # Admin can transfer any account
        elif user_role == "account_owner":
            authorized = src["owner_id"] == user_id
        elif user_role == "customer_service":
            # Customer service typically cannot transfer funds directly
            authorized = False
        else:
            authorized = False

        if not authorized:
            raise PermissionError("User is not authorized to transfer funds from this account.")

        if src["balance"] < amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (f"Transfer of ${amount:,.2f} from {from_account} "
            f"to {to_account} completed successfully.")


# Example usage (uncomment to test)
# try:
#     msg = transfer_funds("user_1", "account_owner", "ACC123", "ACC456", 200.0)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")