import threading
from decimal import Decimal, InvalidOperation

# Sample in‑memory accounts database
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": Decimal("5000.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_456", "balance": Decimal("3000.00")},
    # ... more accounts ...
}

# Global lock to serialize updates (simple concurrency protection)
_db_lock = threading.Lock()


def _get_account(account_number: str):
    """Retrieve account dict or raise KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError:
        raise ValueError(f"Account {account_number} does not exist.")


def _authorize(person_id: str, role: str, source_account: dict) -> bool:
    """
    Determine if the user is authorized to initiate a transfer from source_account.
    * account_owner: must own the source account
    * bank_admin, customer_service: allowed for any account
    """
    if role in {"bank_admin", "customer_service"}:
        return True
    if role == "account_owner" and source_account["owner_id"] == person_id:
        return True
    return False


def move_money(person_id: str, role: str,
               source_account: str, destination_account: str,
               transfer_amount: float) -> str:
    """
    Move money from source_account to destination_account.

    Raises:
        PermissionError: if the user is not authorized.
        ValueError: for invalid accounts or insufficient funds.
    """
    # Validate transfer amount
    try:
        amount = Decimal(str(transfer_amount))
    except InvalidOperation:
        raise ValueError("Invalid transfer amount.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:  # Ensure atomicity of read‑modify‑write
        src = _get_account(source_account)
        dst = _get_account(destination_account)

        # Authorization check
        if not _authorize(person_id, role, src):
            raise PermissionError("Unauthorized access to source account.")

        # Sufficient funds check
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )