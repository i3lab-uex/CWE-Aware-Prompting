from decimal import Decimal, getcontext, InvalidOperation
from typing import Dict

# Set precision high enough for typical financial calculations
getcontext().prec = 28


# Example accounts database.
# In a real system this would be replaced by a persistent datastore.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1500.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("300.00")},
    "ACC003": {"account_number": "ACC003", "owner_id": "user123", "balance": Decimal("200.00")},
}


def _is_authorized(u_id: str, u_role: str, source_acc: Dict, dest_acc: Dict) -> bool:
    """
    Determine if the user is allowed to transfer funds between source and destination accounts.
    Roles:
        - bank_admin: can transfer any accounts
        - account_owner: can transfer only from their own source account
        - customer_service: allowed to transfer only between accounts owned by the same user
    """
    if u_role == "bank_admin":
        return True

    if u_role == "account_owner" and source_acc["owner_id"] == u_id:
        return True

    if (
        u_role == "customer_service"
        and source_acc["owner_id"] == dest_acc["owner_id"]
    ):
        return True

    return False


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer funds from source_account to destination_account.

    Raises:
        PermissionError: If the user is not authorized.
        ValueError: For invalid input data (negative amount, missing accounts).
    """
    # Validate account existence
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise ValueError(f"Source account '{source_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{destination_account}' does not exist.")

    # Convert money to Decimal for accurate arithmetic
    try:
        amount = Decimal(str(money))
    except (InvalidOperation, TypeError):
        raise ValueError("Amount must be a numeric value.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Authorization check
    if not _is_authorized(u_id, u_role, src, dst):
        raise PermissionError("User not authorized to perform this transfer.")

    # Balance check
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )