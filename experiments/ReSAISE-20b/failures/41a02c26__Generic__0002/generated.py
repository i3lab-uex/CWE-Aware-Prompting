import threading

# Sample accounts database (in-memory for this example)
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": 3000.0},
    # Add more accounts as needed
}

# Lock to ensure thread‑safe updates on the shared ACCOUNTS_DB
DB_LOCK = threading.RLock()


def _authorize(uid: str, role: str, source_account: dict) -> bool:
    """
    Determine whether the user is authorized to transfer from the source account.
    - account_owner: must own the source account
    - bank_admin or customer_service: allowed to transfer on behalf of anyone
    """
    if role in {"bank_admin", "customer_service"}:
        return True
    if role == "account_owner" and source_account["owner_id"] == uid:
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
    Transfer money from source_account to destination_account.

    Parameters
    ----------
    uid : str
        ID of the user initiating the transfer.
    role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to withdraw from.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid accounts or insufficient funds.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with DB_LOCK:
        src_acc = ACCOUNTS_DB.get(source_account)
        dst_acc = ACCOUNTS_DB.get(destination_account)

        if src_acc is None or dst_acc is None:
            raise ValueError("One or both accounts do not exist.")

        if not _authorize(uid, role, src_acc):
            raise PermissionError("Unauthorized transfer attempt.")

        if src_acc["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer atomically
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )