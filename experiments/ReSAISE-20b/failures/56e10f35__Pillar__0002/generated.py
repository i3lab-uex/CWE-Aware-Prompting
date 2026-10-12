import threading
from typing import Dict

# Sample accounts database. In a real system this would be persisted securely.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_a", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_b", "balance": 500.0},
    # ... more accounts ...
}

# Lock to serialize access to the shared database and prevent race conditions.
_db_lock = threading.Lock()


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds from `withdraw_account` to `deposit_account`.

    Args:
        initiator_id: ID of the user initiating the transfer.
        position: Role of the initiator ('account_owner', 'bank_admin',
                  or 'customer_service').
        withdraw_account: Account number to debit.
        deposit_account: Account number to credit.
        transfer_value: Amount to transfer.

    Returns:
        Success message upon completion.

    Raises:
        PermissionError: If the initiator is not authorized.
        ValueError: For invalid input or insufficient funds.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")

    # Only account owners and bank admins are allowed to initiate transfers.
    if position not in {"account_owner", "bank_admin"}:
        raise PermissionError(
            f"User {initiator_id} with role '{position}' is not authorized to transfer funds."
        )

    # Acquire lock for atomic check‑modify operations.
    with _db_lock:
        withdraw_acct = ACCOUNTS_DB.get(withdraw_account)
        deposit_acct = ACCOUNTS_DB.get(deposit_account)

        if not withdraw_acct or not deposit_acct:
            raise ValueError("One or both accounts do not exist.")

        # Account owner can only transfer from their own account unless they are admin.
        if position == "account_owner" and withdraw_acct["owner_id"] != initiator_id:
            raise PermissionError(
                f"User {initiator_id} is not the owner of account {withdraw_account}."
            )

        if withdraw_acct["balance"] < transfer_value:
            raise ValueError("Insufficient funds in the withdrawal account.")

        # Perform transfer atomically
        withdraw_acct["balance"] -= transfer_value
        deposit_acct["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully."
    )