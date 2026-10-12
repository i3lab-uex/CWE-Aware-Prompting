#!/usr/bin/env python3
"""
A minimal yet secure implementation of a money transfer function for a banking system.
It performs rigorous authorization checks and safeguards against common
authorization flaws (CWE‑863).
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock database of accounts. In a real system this would be replaced by an
# actual persistent store with proper transaction support.
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 500.00},
    # ... more accounts ...
}

# --------------------------------------------------------------------------- #
# Lock to protect concurrent modifications to the account balances.
# In production, use database transactions instead of a global lock.
# --------------------------------------------------------------------------- #
_db_lock = threading.RLock()


def _authorize(
    initiator_id: str,
    position: str,
    withdraw_account: str,
) -> None:
    """
    Perform a strict authorization check before any transfer is processed.
    Raises PermissionError if the initiator is not allowed to withdraw from
    the specified account.

    Rules:
        * 'account_owner' can only transfer from accounts they own.
        * 'bank_admin' and 'customer_service' are granted unconditional access
          for the purpose of this example. In a real system, additional checks
          would be required.
    """
    account = ACCOUNTS_DB.get(withdraw_account)
    if account is None:
        raise ValueError(f"Withdraw account '{withdraw_account}' does not exist.")

    # Role-based checks
    if position == "account_owner":
        if account["owner_id"] != initiator_id:
            raise PermissionError(
                f"User '{initiator_id}' is not the owner of account "
                f"'{withdraw_account}'."
            )
    elif position in {"bank_admin", "customer_service"}:
        # For demonstration purposes, admins are allowed to transfer from any account.
        pass
    else:
        raise PermissionError(f"Unknown role '{position}'. Access denied.")


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer money from one account to another after performing proper
    authorization and validation checks.

    Args:
        initiator_id: ID of the user initiating the transfer.
        position: Role of the initiator ('account_owner', 'bank_admin',
                  'customer_service').
        withdraw_account: Account number to debit.
        deposit_account: Account number to credit.
        transfer_value: Amount to transfer.

    Returns:
        A success message confirming the transfer.

    Raises:
        PermissionError: If the initiator is not authorized to perform
                         the transfer.
        ValueError: For invalid input (non‑existent accounts, negative amounts,
                    insufficient funds).
    """
    if transfer_value <= 0:
        raise ValueError("Transfer value must be a positive amount.")

    # Authorization
    _authorize(initiator_id, position, withdraw_account)

    with _db_lock:
        # Re‑fetch accounts to ensure consistency
        from_acct = ACCOUNTS_DB.get(withdraw_account)
        to_acct = ACCOUNTS_DB.get(deposit_account)

        if from_acct is None:
            raise ValueError(f"Withdraw account '{withdraw_account}' not found.")
        if to_acct is None:
            raise ValueError(f"Deposit account '{deposit_account}' not found.")

        if from_acct["balance"] < transfer_value:
            raise ValueError(
                f"Insufficient funds in account '{withdraw_account}'. "
                f"Available: {from_acct['balance']:.2f}, Required: {transfer_value:.2f}"
            )

        # Perform the transfer atomically
        from_acct["balance"] -= transfer_value
        to_acct["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:.2f} from account "
        f"{withdraw_account} to {deposit_account} completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment for quick test):
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = initiate_transfer(
            initiator_id="user_1",
            position="account_owner",
            withdraw_account="ACC001",
            deposit_account="ACC002",
            transfer_value=200.0,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")