from decimal import Decimal, InvalidOperation
from typing import Dict

# Example in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

# Roles that are allowed to initiate transfers
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}

def _get_account(account_number: str) -> Dict:
    """Retrieve an account from the database."""
    account = ACCOUNTS_DB.get(account_number)
    if not account:
        raise ValueError(f"Account {account_number} does not exist.")
    return account

def _is_authorized(person_id: str, role: str, source_account: Dict) -> bool:
    """Check whether the user is allowed to transfer from the source account."""
    if role not in ALLOWED_ROLES:
        return False
    # Owner can transfer from their own account
    if role == "account_owner" and source_account["owner_id"] != person_id:
        return False
    # Bank admin or customer service can transfer from any account
    return True

def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Move money from source_account to destination_account.

    Raises:
        PermissionError: If the user is not authorized.
        ValueError: For invalid accounts or insufficient funds.
    """
    # Validate transfer amount
    try:
        amount = Decimal(str(transfer_amount)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        raise ValueError("Transfer amount must be a valid decimal number.")

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    src_acc = _get_account(source_account)
    dst_acc = _get_account(destination_account)

    # Authorization check
    if not _is_authorized(person_id, role, src_acc):
        raise PermissionError("Unauthorized access: insufficient privileges to transfer funds.")

    # Check for sufficient balance
    if src_acc["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src_acc["balance"] -= amount
    dst_acc["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )