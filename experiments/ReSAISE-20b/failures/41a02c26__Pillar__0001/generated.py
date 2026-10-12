#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A minimal banking transfer module that demonstrates proper access control.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock database of accounts. In a real system this would be persisted.
# Each account contains:
#   - account_number: str
#   - owner_id: str
#   - balance: float (in USD)
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_01", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_02", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_03", "balance": 1500.00},
}

# Lock to guard concurrent access to the accounts database
_db_lock = threading.Lock()


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds from *source_account* to *destination_account*.

    Parameters
    ----------
    uid : str
        User ID initiating the transfer.
    role : str
        Role of the user. Must be one of:
            - 'account_owner': can transfer from accounts they own.
            - 'bank_admin'   : can transfer between any accounts.
            - 'customer_service': can perform transfers only if the user owns *source_account*.
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount in USD to transfer.

    Returns
    -------
    str
        Success message with new balances.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid inputs such as non‑existent accounts, negative amounts,
        or insufficient funds.
    """
    # Basic input validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if source_account == destination_account:
        raise ValueError("Source and destination accounts must differ.")

    with _db_lock:
        # Retrieve account records
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None or dst is None:
            raise ValueError("One or both accounts do not exist.")

        # Authorization logic
        if role == "bank_admin":
            authorized = True  # admins can transfer any funds
        elif role == "account_owner" and src["owner_id"] == uid:
            authorized = True
        elif role == "customer_service" and src["owner_id"] == uid:
            authorized = True
        else:
            authorized = False

        if not authorized:
            raise PermissionError("Unauthorized transfer attempt.")

        # Check sufficient funds
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer atomically
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    # Return a clear success message
    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account} "
        f"to {destination_account} completed successfully.\n"
        f"New balances: {source_account}: ${src['balance']:,.2f}, "
        f"{destination_account}: ${dst['balance']:,.2f}"
    )


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid accidental execution)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = process_transfer(
            uid="user_01",
            role="account_owner",
            source_account="ACC1001",
            destination_account="ACC1002",
            transfer_amount=250.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")