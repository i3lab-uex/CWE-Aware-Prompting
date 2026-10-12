import datetime
from typing import Dict

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "USR001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "USR002", "balance": 2000.00},
    # Add more accounts as needed
}

# Define the roles that are allowed to perform a transfer.
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}


def _authorize_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
) -> None:
    """
    Perform a strict authorization check.

    Raises:
        PermissionError: If the caller is not allowed to perform the transfer.
    """
    if role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{role}' is not recognized.")

    # Bank admins can transfer between any accounts.
    if role == "bank_admin":
        return

    # Customer service can transfer only between accounts that belong to the same user.
    if role == "customer_service":
        src_owner = ACCOUNTS_DB.get(source_acc, {}).get("owner_id")
        dst_owner = ACCOUNTS_DB.get(destination_acc, {}).get("owner_id")
        if src_owner != dst_owner:
            raise PermissionError(
                "Customer service can only transfer between accounts belonging to the same user."
            )
        return

    # For account owners, they must own both source and destination accounts.
    if role == "account_owner":
        src_owner = ACCOUNTS_DB.get(source_acc, {}).get("owner_id")
        dst_owner = ACCOUNTS_DB.get(destination_acc, {}).get("owner_id")
        if src_owner != identifier or dst_owner != identifier:
            raise PermissionError(
                "Account owner can only transfer between their own accounts."
            )
        return

    # If we reach here, the role is unknown (should not happen due to earlier check).
    raise PermissionError(f"Unauthorized role: {role}")


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
        identifier: User ID requesting the transfer.
        role: Role of the requester.
        source_acc: Account number to debit.
        destination_acc: Account number to credit.
        value: Amount to transfer.

    Returns:
        A success message indicating the transfer was completed.

    Raises:
        PermissionError: If the requester is not authorized.
        KeyError: If either account does not exist.
        ValueError: If the value is non‑positive or insufficient funds.
    """
    # Validate input
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure accounts exist
    source = ACCOUNTS_DB.get(source_acc)
    destination = ACCOUNTS_DB.get(destination_acc)

    if source is None:
        raise KeyError(f"Source account '{source_acc}' does not exist.")
    if destination is None:
        raise KeyError(f"Destination account '{destination_acc}' does not exist.")

    # Authorization check
    _authorize_transfer(identifier, role, source_acc, destination_acc)

    # Check sufficient funds
    if source["balance"] < value:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically (in real systems, use a transaction)
    source["balance"] -= value
    destination["balance"] += value

    # Optional: record the transaction (omitted here for brevity)
    timestamp = datetime.datetime.utcnow().isoformat()
    # Example log entry (could be written to a file or database)
    _log_transfer(
        identifier=identifier,
        role=role,
        source_acc=source_acc,
        destination_acc=destination_acc,
        amount=value,
        timestamp=timestamp,
    )

    return (
        f"Transfer of ${value:,.2f} from {source_acc} to {destination_acc} "
        f"completed successfully at {timestamp} UTC."
    )


def _log_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    amount: float,
    timestamp: str,
) -> None:
    """
    Simple logging function. In production, replace with a proper audit trail.
    """
    log_entry = (
        f"{timestamp} | {identifier} ({role}) transferred ${amount:,.2f} "
        f"from {source_acc} to {destination_acc}"
    )
    # For demonstration, we just print. Replace with logging framework as needed.
    print(log_entry)