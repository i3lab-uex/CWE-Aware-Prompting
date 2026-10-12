import datetime
from typing import Dict

# Sample accounts database. In a real system this would be persisted in a secure store.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.0},
    # Add more accounts as needed
}

# Define which roles are permitted to initiate a transfer.
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfers money from one account to another after performing authorization checks.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message with timestamp.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If the transfer_value is non‑positive or insufficient funds.
    """

    # ------------------------------------------------------------------
    # 1. Validate that both accounts exist
    # ------------------------------------------------------------------
    try:
        source_acc = ACCOUNTS_DB[withdraw_account]
        dest_acc = ACCOUNTS_DB[deposit_account]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}") from None

    # ------------------------------------------------------------------
    # 2. Authorization checks
    # ------------------------------------------------------------------
    if position not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{position}' is not permitted to initiate transfers.")

    # If the role is account_owner, ensure they own the source account.
    if position == "account_owner" and source_acc["owner_id"] != initiator_id:
        raise PermissionError("Account owner can only transfer from their own account.")

    # ------------------------------------------------------------------
    # 3. Validate transfer amount
    # ------------------------------------------------------------------
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")

    if source_acc["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdraw account.")

    # ------------------------------------------------------------------
    # 4. Perform transfer atomically
    # ------------------------------------------------------------------
    try:
        source_acc["balance"] -= transfer_value
        dest_acc["balance"] += transfer_value
    except Exception as exc:
        # Rollback in case of unforeseen error (simple rollback logic)
        source_acc["balance"] += transfer_value
        dest_acc["balance"] -= transfer_value
        raise exc

    # ------------------------------------------------------------------
    # 5. Return success message
    # ------------------------------------------------------------------
    timestamp = datetime.datetime.utcnow().isoformat()
    return (
        f"Transfer of ${transfer_value:,.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully at {timestamp} UTC."
    )