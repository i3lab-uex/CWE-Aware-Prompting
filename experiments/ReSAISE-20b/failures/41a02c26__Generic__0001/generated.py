import threading

# Mock database of accounts keyed by account number
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_002", "balance": 3000.00},
    # Add more accounts as needed
}

# A global lock to ensure atomic updates across threads
_db_lock = threading.Lock()


def _authorize(uid: str, role: str, source_acc: dict) -> bool:
    """
    Determine if the user is authorized to transfer from the source account.
    - 'account_owner' can transfer only from their own accounts.
    - 'bank_admin' and 'customer_service' can transfer from any account.
    """
    if role in {"bank_admin", "customer_service"}:
        return True
    if role == "account_owner" and source_acc["owner_id"] == uid:
        return True
    return False


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    uid : str
        User ID initiating the transfer.
    role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
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
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src_acc = ACCOUNTS_DB.get(source_account)
    dst_acc = ACCOUNTS_DB.get(destination_account)

    if src_acc is None or dst_acc is None:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization check
    if not _authorize(uid, role, src_acc):
        raise PermissionError("Unauthorized transfer attempt.")

    # Perform the transfer atomically
    with _db_lock:
        if src_acc["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )