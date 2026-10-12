import decimal
from typing import Dict

# Sample in‑memory accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U123", "balance": decimal.Decimal("5000.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U456", "balance": decimal.Decimal("3000.00")},
    # Add more accounts as needed
}

def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Transfer money from source_account to destination_account.

    Raises PermissionError if the user is not authorized.
    Raises KeyError if an account does not exist.
    Raises ValueError for insufficient funds or invalid amount.

    Returns a success message on completion.
    """
    # Validate transfer_amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Convert to Decimal for accurate arithmetic
    amount = decimal.Decimal(str(transfer_amount))

    # Authorization: only account owners or bank admins can move money
    if role not in {"account_owner", "bank_admin"}:
        raise PermissionError("Unauthorized: Only account owners or bank admins can perform transfers.")

    # Fetch accounts
    try:
        src_acc = ACCOUNTS_DB[source_account]
        dst_acc = ACCOUNTS_DB[destination_account]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}")

    # If role is account_owner, ensure they own the source account
    if role == "account_owner" and src_acc["owner_id"] != person_id:
        raise PermissionError("Unauthorized: You do not own the source account.")

    # Check sufficient funds
    if src_acc["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform transfer atomically (in this simple example, just two updates)
    src_acc["balance"] -= amount
    dst_acc["balance"] += amount

    return (
        f"Success: Transferred {amount:.2f} from {source_account} "
        f"to {destination_account}. New balance: {src_acc['balance']:.2f}"
    )