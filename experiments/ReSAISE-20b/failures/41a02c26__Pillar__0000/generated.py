import threading

# Example accounts database (in a real system this would be a persistent store)
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # ... other accounts
}

# A global lock to protect concurrent updates to the account balances.
_ACCOUNTS_LOCK = threading.Lock()


def process_transfer(uid: str, role: str,
                     source_account: str, destination_account: str,
                     transfer_amount: float) -> str:
    """
    Transfer money from source_account to destination_account.

    Parameters
    ----------
    uid : str
        User ID of the requester.
    role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service', ...).
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message.

    Raises
    ------
    PermissionError
        If the caller is not authorized to perform the transfer.
    ValueError
        For invalid input such as negative amounts or nonexistent accounts.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization: only the owner of source account, a bank admin,
    # or a customer service role with proper approval can transfer.
    if not (
        (role == "account_owner" and src["owner_id"] == uid) or
        role == "bank_admin"
    ):
        raise PermissionError("Unauthorized transfer attempt.")

    # Ensure sufficient funds
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    with _ACCOUNTS_LOCK:
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from "
        f"{source_account} to {destination_account} completed successfully."
    )