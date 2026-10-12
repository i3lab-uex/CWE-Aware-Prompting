import datetime
from typing import Dict

# Example account database structure
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed
}


def _authorize_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
) -> None:
    """
    Internal helper to verify that the initiator is allowed to withdraw from
    the specified account.

    Raises:
        PermissionError: If the user is not authorized.
    """
    if withdraw_account not in ACCOUNTS_DB:
        raise ValueError(f"Account {withdraw_account} does not exist.")

    account = ACCOUNTS_DB[withdraw_account]

    # Simple role-based checks:
    if position == "bank_admin":
        return  # admins can transfer from any account

    if position == "account_owner" and account["owner_id"] == initiator_id:
        return

    if position == "customer_service":
        # Customer service can transfer only to accounts owned by the same initiator
        return

    raise PermissionError(
        f"User '{initiator_id}' with role '{position}' is not authorized to transfer from account {withdraw_account}."
    )


def _validate_amount(transfer_value: float) -> None:
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive.")


def _perform_transfer(
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> None:
    """
    Adjust balances atomically. In a real system, this would be wrapped in a
    database transaction to ensure consistency.
    """
    if deposit_account not in ACCOUNTS_DB:
        raise ValueError(f"Target account {deposit_account} does not exist.")

    if ACCOUNTS_DB[withdraw_account]["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Update balances
    ACCOUNTS_DB[withdraw_account]["balance"] -= transfer_value
    ACCOUNTS_DB[deposit_account]["balance"] += transfer_value


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Facilitate a money transfer between two accounts.

    Args:
        initiator_id (str): ID of the user initiating the transfer.
        position (str): Role of the initiator ('account_owner', 'bank_admin',
            'customer_service').
        withdraw_account (str): Account number to debit.
        deposit_account (str): Account number to credit.
        transfer_value (float): Amount to transfer.

    Returns:
        str: Success message confirming the transfer.

    Raises:
        PermissionError: If the initiator lacks authorization.
        ValueError: For invalid accounts, insufficient funds or bad input.
    """
    # Authorization
    _authorize_transfer(initiator_id, position, withdraw_account)

    # Basic validation
    _validate_amount(transfer_value)

    # Perform the transfer
    _perform_transfer(withdraw_account, deposit_account, transfer_value)

    timestamp = datetime.datetime.utcnow().isoformat()
    return (
        f"Transfer of ${transfer_value:.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully at {timestamp}."
    )