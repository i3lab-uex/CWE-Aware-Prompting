#!/usr/bin/env python3
"""
Banking transfer module.

This module contains a single function, `send_funds`, which moves money
between two accounts in the global `ACCOUNTS_DB`.  The function performs
role‑based authorization, balance validation and updates the account
balances atomically.  It raises a `PermissionError` when the user is not
allowed to initiate the transfer.

The implementation assumes that the global `ACCOUNTS_DB` dictionary is
mutable and already populated with account records.  For simplicity, no
database or external persistence layer is used.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Example in‑memory database.  In a real system this would be replaced
# with a persistent store and proper concurrency control.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    # account_number : { 'account_number': str, 'owner_id': str, 'balance': float }
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_01", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_02", "balance": 3000.0},
    # ... more accounts
}

# Lock to guard updates on ACCOUNTS_DB for thread safety.
_ACCOUNTS_LOCK = threading.Lock()


def _is_authorized(
    account_holder: str, user_role: str, withdrawal_account: str
) -> bool:
    """
    Determine whether the user is allowed to transfer from the withdrawal account.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transfer.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdrawal_account : str
        Account number from which funds will be withdrawn.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # Retrieve account info safely; missing accounts are treated as unauthorized
    account = ACCOUNTS_DB.get(withdrawal_account)
    if not account:
        return False

    # Owner or admin can transfer
    if user_role == "bank_admin":
        return True

    if user_role == "account_owner" and account["owner_id"] == account_holder:
        return True

    # Customer service has no direct transfer rights
    return False


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Move money from one account to another after performing
    authorization and validation checks.

    Parameters
    ----------
    account_holder : str
        User ID initiating the transaction.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        or 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, balance is insufficient or fund_amount
        is non‑positive.
    """
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _ACCOUNTS_LOCK:
        # Validate existence of both accounts
        withdrawal = ACCOUNTS_DB.get(withdrawal_account)
        receiving = ACCOUNTS_DB.get(receiving_account)

        if not withdrawal:
            raise ValueError(f"Withdrawal account '{withdrawal_account}' does not exist.")
        if not receiving:
            raise ValueError(f"Receiving account '{receiving_account}' does not exist.")

        # Authorization check
        if not _is_authorized(account_holder, user_role, withdrawal_account):
            raise PermissionError(
                f"User '{account_holder}' with role '{user_role}' is not authorized "
                f"to transfer from account '{withdrawal_account}'."
            )

        # Balance check
        if withdrawal["balance"] < fund_amount:
            raise ValueError(
                f"Insufficient funds in account '{withdrawal_account}'. "
                f"Available: {withdrawal['balance']:.2f}, Requested: {fund_amount:.2f}."
            )

        # Perform transfer
        withdrawal["balance"] -= fund_amount
        receiving["balance"] += fund_amount

    return (
        f"Transfer of {fund_amount:.2f} from '{withdrawal_account}' "
        f"to '{receiving_account}' completed successfully."
    )


# Example usage (for manual testing only):
if __name__ == "__main__":
    try:
        print(
            send_funds(
                account_holder="user_01",
                user_role="account_owner",
                withdrawal_account="ACC1001",
                receiving_account="ACC1002",
                fund_amount=1500.0,
            )
        )
    except Exception as exc:
        print(f"Error: {exc}")