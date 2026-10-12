import datetime

# Sample account database (in a real system this would be replaced by persistent storage)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1000.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 500.00},
    "ACC003": {"account_number": "ACC003", "owner_id": "user_3", "balance": 2000.00},
}

# Simple role-based permissions mapping
ROLE_PERMISSIONS = {
    "account_owner": {"transfer_own"},
    "bank_admin": {"transfer_any"},
    "customer_service": {"transfer_any"},
}

def _has_permission(position: str, permission: str) -> bool:
    """Return True if the role has the specified permission."""
    return permission in ROLE_PERMISSIONS.get(position, set())

def _log_transfer(initiator_id: str,
                  withdraw_account: str,
                  deposit_account: str,
                  amount: float) -> None:
    """Persist a transfer record. In production this would write to an audit log."""
    # For demonstration we simply print the log entry
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] Transfer by {initiator_id}: "
          f"{amount} from {withdraw_account} to {deposit_account}")

def initiate_transfer(initiator_id: str,
                      position: str,
                      withdraw_account: str,
                      deposit_account: str,
                      transfer_value: float) -> str:
    """
    Transfer money from one account to another after performing a correct
    authorization check.

    Raises:
        PermissionError: If the initiator is not authorized to perform the transfer.
        ValueError: If account numbers are invalid or insufficient funds.
    """
    # Validate accounts exist
    src = ACCOUNTS_DB.get(withdraw_account)
    dst = ACCOUNTS_DB.get(deposit_account)

    if not src or not dst:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization logic
    if position == "account_owner":
        # Owner can transfer only from their own account
        if src["owner_id"] != initiator_id:
            raise PermissionError("Account owners can transfer only from their own accounts.")
    elif position in {"bank_admin", "customer_service"}:
        # These roles can transfer between any accounts
        pass
    else:
        raise PermissionError("Unrecognized role; access denied.")

    # Check sufficient funds
    if src["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer
    src["balance"] -= transfer_value
    dst["balance"] += transfer_value

    # Log the transaction (important for auditability)
    _log_transfer(initiator_id, withdraw_account, deposit_account, transfer_value)

    return (f"Transfer of ${transfer_value:.2f} from {withdraw_account} "
            f"to {deposit_account} completed successfully.")