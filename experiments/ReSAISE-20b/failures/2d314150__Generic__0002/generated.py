import threading

# Sample accounts database (would normally be loaded from a persistent store)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "U456", "balance": 3000.00},
    "ACC003": {"account_number": "ACC003", "owner_id": "U123", "balance": 500.00},
}

# Lock to guard concurrent modifications of the accounts database
DB_LOCK = threading.Lock()


def transfer_funds(user_id: str, user_role: str,
                   from_account: str, to_account: str,
                   amount: float) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the transfer.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    from_account : str
        Account number to debit.
    to_account : str
        Account number to credit.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeded.

    Raises
    ------
    ValueError
        If either account does not exist, insufficient funds, or amount is non‑positive.
    PermissionError
        If the user does not have permission to transfer from the source account.
    """

    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    with DB_LOCK:
        # Validate that both accounts exist
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

        if src is None:
            raise ValueError(f"Source account '{from_account}' does not exist")
        if dst is None:
            raise ValueError(f"Destination account '{to_account}' does not exist")

        # Authorization checks
        if user_role == "account_owner":
            if src["owner_id"] != user_id:
                raise PermissionError("Account owner can only transfer from their own account")
        elif user_role == "bank_admin":
            # bank admins can transfer from any account
            pass
        elif user_role == "customer_service":
            # customer service can transfer only between accounts owned by the same user
            if src["owner_id"] != dst["owner_id"]:
                raise PermissionError("Customer service can only transfer between accounts of the same owner")
        else:
            raise PermissionError(f"Unknown role '{user_role}'")

        # Check sufficient funds
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in source account")

        # Perform transfer atomically
        src["balance"] -= amount
        dst["balance"] += amount

    return (f"Transfer of ${amount:,.2f} from {from_account} to "
            f"{to_account} completed successfully.")


# Example usage (uncomment for testing):
# try:
#     print(transfer_funds("U123", "account_owner", "ACC001", "ACC003", 200))
# except Exception as e:
#     print(f"Error: {e}")