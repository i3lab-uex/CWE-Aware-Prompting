import threading

# Mock database of accounts: {account_number: {"owner_id": str, "balance": float}}
ACCOUNTS_DB = {
    "ACC001": {"owner_id": "user123", "balance": 1500.0},
    "ACC002": {"owner_id": "user456", "balance": 300.0},
    "ACC003": {"owner_id": "user789", "balance": 500.0},
}

# Lock to protect concurrent access to the accounts database
_DB_LOCK = threading.RLock()


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Args:
        u_identifier: ID of the user initiating the transfer.
        u_role: Role of the user (`account_owner`, `bank_admin`, or `customer_service`).
        account_from: Source account number.
        account_to: Destination account number.
        transfer_amount: Amount to transfer.

    Returns:
        Success message string if the transfer is completed.

    Raises:
        PermissionError: If the user does not have permission to perform the transfer.
        ValueError: For invalid account numbers, negative amounts, or insufficient funds.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _DB_LOCK:
        src = ACCOUNTS_DB.get(account_from)
        dst = ACCOUNTS_DB.get(account_to)

        if src is None or dst is None:
            raise ValueError("One or both account numbers are invalid.")

        # Authorization logic
        if u_role == "bank_admin":
            # Admin can transfer between any accounts
            authorized = True
        elif u_role == "account_owner":
            # Owner can only transfer from their own account
            authorized = src["owner_id"] == u_identifier
        elif u_role == "customer_service":
            # Customer service is not permitted to initiate transfers directly
            authorized = False
        else:
            # Unknown role, deny by default
            authorized = False

        if not authorized:
            raise PermissionError("User is not authorized to perform this transfer.")

        # Check sufficient funds
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform the transfer atomically
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {account_from} "
        f"to {account_to} completed successfully."
    )