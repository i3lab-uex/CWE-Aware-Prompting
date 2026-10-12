import threading
from typing import Dict

# Simulated in‑memory accounts database.
# In a real system this would be persisted in a secure database.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_456", "balance": 3000.00},
    # Add more accounts as needed.
}

# A lock per account to prevent race conditions during concurrent transfers.
_account_locks: Dict[str, threading.Lock] = {
    acc_no: threading.Lock() for acc_no in ACCOUNTS_DB
}


def _authorize(uid: str, role: str, source_account: str) -> None:
    """
    Checks whether the user identified by uid with a given role is allowed to
    initiate a transfer from source_account.

    Raises:
        PermissionError: if the user is not authorized.
    """
    account = ACCOUNTS_DB.get(source_account)
    if account is None:
        raise ValueError(f"Source account {source_account} does not exist.")

    # Authorization logic:
    #   • bank_admin can transfer from any account.
    #   • account_owner can transfer only from their own account.
    if role == "bank_admin":
        return
    if role == "account_owner" and uid == account["owner_id"]:
        return

    raise PermissionError("Unauthorized transfer attempt.")


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Performs a money transfer between two accounts after validating
    authorization, account existence, and sufficient funds.

    Args:
        uid: User ID initiating the transfer.
        role: Role of the user (e.g., 'account_owner', 'bank_admin').
        source_account: Account number to debit.
        destination_account: Account number to credit.
        transfer_amount: Amount to transfer.

    Returns:
        A confirmation message on success.

    Raises:
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: For invalid accounts or insufficient funds.
    """
    # Basic input validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Authorization check
    _authorize(uid, role, source_account)

    # Verify destination account exists
    dest_acc = ACCOUNTS_DB.get(destination_account)
    if dest_acc is None:
        raise ValueError(f"Destination account {destination_account} does not exist.")

    # Acquire locks for both accounts in a consistent order to avoid deadlocks.
    first_lock, second_lock = (
        (_account_locks[source_account], _account_locks[destination_account])
        if source_account < destination_account
        else (_account_locks[destination_account], _account_locks[source_account])
    )

    with first_lock, second_lock:
        src_acc = ACCOUNTS_DB[source_account]
        if src_acc["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the debit and credit atomically
        src_acc["balance"] -= transfer_amount
        dest_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )