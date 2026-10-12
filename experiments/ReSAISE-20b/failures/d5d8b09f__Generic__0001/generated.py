#!/usr/bin/env python3
"""
Banking system – fund transfer module.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Dummy in‑memory accounts database. In a real system this would be
# replaced by persistent storage (e.g., SQL, NoSQL) with proper isolation.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}

# Simple lock to protect concurrent modifications of the in‑memory DB.
_db_lock = threading.Lock()


def _get_account(account_number: str) -> Dict[str, Any]:
    """Retrieve an account from the database or raise KeyError."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
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
        If the user is not authorized to perform this transfer.
    ValueError
        If accounts do not exist or if the withdrawal account lacks sufficient funds.
    """
    # Basic validation
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts (will raise ValueError if missing)
    with _db_lock:
        withdraw_acc = _get_account(withdrawal_account)
        receive_acc = _get_account(receiving_account)

        # Authorization checks
        if user_role == "bank_admin":
            authorized = True
        elif user_role == "account_owner" and withdraw_acc["owner_id"] == account_holder:
            authorized = True
        elif user_role == "customer_service":
            # Customer service may only perform transfers between accounts owned by the same user
            authorized = (
                withdraw_acc["owner_id"] == account_holder
                and receive_acc["owner_id"] == account_holder
            )
        else:
            authorized = False

        if not authorized:
            raise PermissionError(
                f"User '{account_holder}' with role '{user_role}' "
                "is not authorized to perform this transfer."
            )

        # Sufficient funds check
        if withdraw_acc["balance"] < fund_amount:
            raise ValueError(
                f"Insufficient funds in account {withdrawal_account}. "
                f"Available: {withdraw_acc['balance']}, requested: {fund_amount}."
            )

        # Perform the transfer atomically
        withdraw_acc["balance"] -= fund_amount
        receive_acc["balance"] += fund_amount

    return (
        f"Transfer of {fund_amount:.2f} from account "
        f"{withdrawal_account} to {receiving_account} completed successfully."
    )