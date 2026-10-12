import threading
from typing import Dict

# Sample accounts database (in a real system this would be persisted elsewhere)
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_01", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_02", "balance": 3000.0},
    # Add more accounts as needed
}

# Global lock to protect concurrent modifications of the accounts database
_ACCOUNTS_LOCK = threading.Lock()


def _authorize_transfer(
    identifier: str,
    role: str,
    source_acc: str,
) -> None:
    """
    Verify that the user identified by `identifier` and with role `role`
    is allowed to initiate a transfer from `source_acc`.

    Raises:
        PermissionError: if the user is not authorized.
    """
    # Check that the source account exists
    src_account = ACCOUNTS_DB.get(source_acc)
    if not src_account:
        raise ValueError(f"Source account {source_acc} does not exist.")

    # Authorization logic
    if role == "bank_admin":
        # Admins can transfer from any account
        return

    if role == "account_owner":
        # Owner must own the source account
        if src_account["owner_id"] != identifier:
            raise PermissionError(
                f"User {identifier} does not own source account {source_acc}."
            )
        return

    # Other roles (e.g., customer_service) are not allowed to transfer funds
    raise PermissionError(
        f"Role '{role}' is not authorized to initiate transfers."
    )


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float,
) -> str:
    """
    Transfer money between two accounts.

    Args:
        identifier: The unique ID of the user requesting the transfer.
        role: The role of the user ('account_owner', 'bank_admin',
              'customer_service', etc.).
        source_acc: Account number to debit.
        destination_acc: Account number to credit.
        value: Amount to transfer (must be positive).

    Returns:
        A success message string.

    Raises:
        PermissionError: If the user is not authorized to perform the transfer.
        ValueError: For invalid accounts, insufficient funds, or negative amounts.
    """
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist and are distinct
    with _ACCOUNTS_LOCK:
        src_account = ACCOUNTS_DB.get(source_acc)
        dst_account = ACCOUNTS_DB.get(destination_acc)

        if not src_account:
            raise ValueError(f"Source account {source_acc} does not exist.")
        if not dst_account:
            raise ValueError(f"Destination account {destination_acc} does not exist.")
        if source_acc == destination_acc:
            raise ValueError("Source and destination accounts must differ.")

        # Authorization check
        _authorize_transfer(identifier, role, source_acc)

        # Check sufficient funds
        if src_account["balance"] < value:
            raise ValueError(
                f"Insufficient funds in source account {source_acc}."
            )

        # Perform the transfer atomically
        src_account["balance"] -= value
        dst_account["balance"] += value

    return (
        f"Transfer of {value:.2f} from {source_acc} "
        f"to {destination_acc} completed successfully."
    )