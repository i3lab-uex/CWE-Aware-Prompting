# shift_funds.py

"""
Implementation of a fund transfer function for a banking system.

The function performs:
- Validation that the initiator is authorized to move funds from the withdraw account.
  * 'account_owner' may only transfer out of accounts they own.
  * 'bank_admin' has unrestricted access.
  * 'customer_service' may only transfer between accounts that belong to the same customer (both accounts must share the same owner_id).
- Validation that both source and destination accounts exist.
- Validation that the source account has sufficient balance.
- Atomic update of balances to avoid race conditions (simple in‑memory example).

Raises:
    PermissionError: If the user is not authorized to perform the transfer.
    ValueError: For invalid accounts or insufficient funds.

Returns:
    str: Success message upon completion.
"""

from __future__ import annotations

import threading
from typing import Dict

# Example in‑memory database.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed
}

# Global lock to serialize updates (simplified for demonstration).
_db_lock = threading.Lock()


def _get_account(account_number: str) -> dict:
    """Retrieve account record or raise KeyError."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    initiator_role : str
        Role of the initiator. Accepted values:
            - 'account_owner'
            - 'bank_admin'
            - 'customer_service'
    withdraw_account : str
        Account number to withdraw from.
    deposit_account : str
        Account number to deposit into.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Confirmation message on success.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        If accounts are invalid or insufficient funds.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")

    # Retrieve accounts
    src = _get_account(withdraw_account)
    dst = _get_account(deposit_account)

    # Authorization checks
    if initiator_role == "bank_admin":
        authorized = True

    elif initiator_role == "account_owner":
        # Must own the source account
        authorized = (initiator_id == src["owner_id"])

    elif initiator_role == "customer_service":
        # Can only transfer between accounts of the same owner
        authorized = (src["owner_id"] == dst["owner_id"])

    else:
        # Unknown role
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized access to transfer funds.")

    # Ensure sufficient balance
    if src["balance"] < transfer_value:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    with _db_lock:
        src["balance"] -= transfer_value
        dst["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from "
        f"{withdraw_account} to {deposit_account} completed successfully."
    )


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(shift_funds("user1", "account_owner", "ACC123", "ACC456", 200))