#!/usr/bin/env python3
"""
Implementation of a simple funds transfer function with proper access control.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 750.00},
    # Add more accounts as needed.
}

# Lock to protect concurrent access to the database
_db_lock = threading.RLock()


def _has_permission(u_id: str, u_role: str, source_account: str) -> bool:
    """
    Determine if the user has permission to initiate a transfer from source_account.
    Bank admins and customer service can transfer any account.
    Account owners can only transfer from their own accounts.
    """
    if u_role in {"bank_admin", "customer_service"}:
        return True

    account = ACCOUNTS_DB.get(source_account)
    if not account:
        # Source account does not exist; treat as no permission.
        return False

    return account["owner_id"] == u_id


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer `money` from `source_account` to `destination_account`.

    Parameters
    ----------
    u_id : str
        Identifier of the user requesting the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    money : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the amount transferred and new balances.

    Raises
    ------
    PermissionError
        If the user is not authorized to transfer from `source_account`.
    ValueError
        If either account does not exist, the amount is invalid,
        or insufficient funds are available.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None:
            raise ValueError(f"Source account '{source_account}' does not exist.")
        if dst is None:
            raise ValueError(f"Destination account '{destination_account}' does not exist.")

        if not _has_permission(u_id, u_role, source_account):
            raise PermissionError(
                f"User '{u_id}' with role '{u_role}' is not authorized to transfer from account '{source_account}'."
            )

        if src["balance"] < money:
            raise ValueError(
                f"Insufficient funds in account '{source_account}'. Available: {src['balance']:.2f}"
            )

        # Perform the transfer atomically
        src["balance"] -= money
        dst["balance"] += money

    return (
        f"Transfer of {money:.2f} from '{source_account}' to "
        f"'{destination_account}' completed successfully.\n"
        f"New balance of '{source_account}': {src['balance']:.2f}\n"
        f"New balance of '{destination_account}': {dst['balance']:.2f}"
    )