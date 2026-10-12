# -*- coding: utf-8 -*-
"""
Banking transfer module.

The `process_transfer` function implements a basic money‑transfer
operation while enforcing proper access control (CWE-284).
"""

from __future__ import annotations

import datetime
from typing import Dict, Any

# Mock database of accounts.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1500.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 2500.00},
    # Add more accounts as needed.
}


def _get_account(account_number: str) -> Dict[str, Any]:
    """Retrieve an account from the database. Raise KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc


def _authorize_transfer(
    uid: str, role: str, source_account: Dict[str, Any]
) -> None:
    """
    Ensure the caller is authorized to withdraw from the source account.

    Raises PermissionError if unauthorized.
    """
    # Bank admins and customer service can transfer from any account.
    privileged_roles = {"bank_admin", "customer_service"}
    if role in privileged_roles:
        return

    # Account owners can only transfer from their own accounts.
    if role == "account_owner" and source_account["owner_id"] == uid:
        return

    # All other cases are forbidden.
    raise PermissionError(
        f"User '{uid}' with role '{role}' is not authorized to transfer from account {source_account['account_number']}."
    )


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    uid : str
        User ID initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid accounts, negative amounts, or insufficient funds.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = _get_account(source_account)
    dst = _get_account(destination_account)

    # Authorization check
    _authorize_transfer(uid, role, src)

    # Sufficient funds check
    if src["balance"] < transfer_amount:
        raise ValueError(
            f"Insufficient funds in source account {source_account}."
        )

    # Perform the transfer atomically (simple simulation)
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    # Log the transaction (simple console log; replace with real audit in production)
    timestamp = datetime.datetime.utcnow().isoformat()
    print(
        f"[{timestamp}] Transfer: {transfer_amount} from {source_account} to {destination_account} by user '{uid}' (role: {role})."
    )

    return (
        f"Transfer of ${transfer_amount:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )