from __future__ import annotations
from typing import Dict

# Example account database structure.
# In a real system this would be replaced with secure storage (e.g., a database).
ACCOUNTS_DB: Dict[str, Dict[str, object]] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 5000.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 3000.00},
    # ... additional accounts
}

def _is_authorized(identifier: str, role: str, source_acc: str) -> bool:
    """
    Determine if the user is allowed to initiate a transfer from `source_acc`.

    Rules:
        * 'account_owner' can only transfer from accounts they own.
        * 'bank_admin' and 'customer_service' have full authority.
    """
    if role in {"bank_admin", "customer_service"}:
        return True

    account = ACCOUNTS_DB.get(source_acc)
    if not account:
        # If the source account does not exist, treat as unauthorized
        return False

    return account.get("owner_id") == identifier


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float
) -> str:
    """
    Transfer `value` from `source_acc` to `destination_acc`.

    Raises:
        PermissionError: If the caller is not authorized.
        KeyError: If either account does not exist.
        ValueError: If the source balance is insufficient or if `value` <= 0.

    Returns:
        A success message string.
    """
    # Basic input validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    src = ACCOUNTS_DB.get(source_acc)
    dst = ACCOUNTS_DB.get(destination_acc)

    if src is None or dst is None:
        missing = [acc for acc, acct in [(source_acc, src), (destination_acc, dst)] if acct is None]
        raise KeyError(f"Account(s) not found: {', '.join(missing)}")

    # Authorization check
    if not _is_authorized(identifier, role, source_acc):
        raise PermissionError(f"User '{identifier}' with role '{role}' is not authorized to transfer from account {source_acc}.")

    # Check sufficient funds
    if src["balance"] < value:
        raise ValueError(f"Insufficient funds in account {source_acc}. Current balance: {src['balance']:.2f}")

    # Perform the transfer atomically (in real code, use a transaction)
    src["balance"] -= value
    dst["balance"] += value

    return (
        f"Transfer of {value:.2f} from account {source_acc} "
        f"to account {destination_acc} completed successfully."
    )