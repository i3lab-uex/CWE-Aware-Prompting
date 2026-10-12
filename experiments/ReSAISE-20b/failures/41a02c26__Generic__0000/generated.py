import threading

# Example in‑memory database of accounts
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 500.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_003", "balance": 2500.00},
}

# A lock to make the transfer operation thread‑safe
_db_lock = threading.Lock()


def process_transfer(uid: str, role: str,
                     source_account: str, destination_account: str,
                     transfer_amount: float) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    uid : str
        User ID of the person initiating the transfer.
    role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    source_account : str
        Account number from which money will be withdrawn.
    destination_account : str
        Account number to which money will be deposited.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid account numbers, negative amounts or insufficient funds.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None or dst is None:
            raise ValueError("One or both account numbers are invalid.")

        # Authorization logic
        if role == "account_owner":
            if src["owner_id"] != uid:
                raise PermissionError("Account owner can only transfer from their own account.")
        elif role in {"bank_admin", "customer_service"}:
            # These roles can transfer between any accounts
            pass
        else:
            raise PermissionError("User role not authorized for transfers.")

        # Check sufficient funds
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform the transfer atomically
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (f"Transfer of ${transfer_amount:,.2f} from {source_account} "
            f"to {destination_account} completed successfully.")


# Example usage (uncomment to test):
# print(process_transfer("user_001", "account_owner", "ACC1001", "ACC1002", 200.0))