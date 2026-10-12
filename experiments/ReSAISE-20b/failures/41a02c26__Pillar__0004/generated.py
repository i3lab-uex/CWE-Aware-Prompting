#!/usr/bin/env python3
"""
A minimal banking transfer module with proper access control.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Mock database of accounts.
# In a real system this would be replaced with persistent storage.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_a", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_b", "balance": 3000.0},
    # Add more accounts as needed.
}

# A lock per account to guard concurrent modifications.
ACCOUNT_LOCKS: Dict[str, threading.Lock] = {
    acc_no: threading.Lock() for acc_no in ACCOUNTS_DB
}


def _authorize(uid: str, role: str, source_account: str) -> bool:
    """
    Determine whether the user is allowed to transfer from the source account.

    * `account_owner` may only transfer from accounts they own.
    * `bank_admin` and `customer_service` are allowed to transfer from any account.
    """
    if role in {"bank_admin", "customer_service"}:
        return True

    # For account_owner, check ownership.
    if role == "account_owner":
        owner_id = ACCOUNTS_DB.get(source_account, {}).get("owner_id")
        return uid == owner_id

    # Unknown role -> deny.
    return False


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from `source_account` to `destination_account`.

    Parameters
    ----------
    uid : str
        ID of the user initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to credit funds to.
    transfer_amount : float
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
        If accounts do not exist, the amount is invalid, or insufficient funds.
    """
    # Basic validation of arguments
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    src_acc = ACCOUNTS_DB.get(source_account)
    dst_acc = ACCOUNTS_DB.get(destination_account)

    if src_acc is None or dst_acc is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization check
    if not _authorize(uid, role, source_account):
        raise PermissionError(
            f"User {uid} with role '{role}' is not authorized to transfer from account {source_account}"
        )

    # Acquire locks for both accounts in a consistent order to avoid deadlocks
    first_lock, second_lock = (
        (ACCOUNT_LOCKS[source_account], ACCOUNT_LOCKS[destination_account])
        if source_account < destination_account
        else (ACCOUNT_LOCKS[destination_account], ACCOUNT_LOCKS[source_account])
    )

    with first_lock, second_lock:
        # Re-check balance after acquiring lock
        if src_acc["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer atomically
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )