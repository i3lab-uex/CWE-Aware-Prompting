#!/usr/bin/env python3
"""
Financial transfer helper – move_funds

This module contains a single public function `move_funds` that
performs a funds transfer between two accounts in an in‑memory
database `ACCOUNTS_DB`.  The function includes basic security checks,
error handling, and uses a thread‑safe lock to protect the shared
state.

Author: ChatGPT
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory account database (simulated)
# --------------------------------------------------------------------------- #

ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 750.00},
}

# --------------------------------------------------------------------------- #
# Thread‑safety lock for the shared database
# --------------------------------------------------------------------------- #

_db_lock = threading.Lock()


def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account dictionary from ACCOUNTS_DB.
    Raises KeyError if the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account '{account_number}' does not exist.") from exc


def _validate_funds(source: Dict[str, Any], amount: float) -> None:
    """
    Ensure the source account has sufficient balance for the transfer.
    Raises ValueError if insufficient funds.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if source["balance"] < amount:
        raise ValueError(
            f"Insufficient funds: available {source['balance']:.2f}, required {amount:.2f}."
        )


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
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user. Only 'account_owner' is allowed to initiate a transfer.
    source_account : str
        Account number from which funds will be withdrawn.
    destination_account : str
        Account number to which funds will be deposited.
    money : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message describing the completed transaction.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the transfer amount is invalid or insufficient funds are available.
    """
    # 1. Authorization check
    if u_role != "account_owner":
        raise PermissionError(
            f"User role '{u_role}' is not authorized to move funds."
        )

    # 2. Acquire lock for atomic update
    with _db_lock:
        # 3. Retrieve accounts (will raise KeyError if not found)
        src_acc = _get_account(source_account)
        dst_acc = _get_account(destination_account)

        # 4. Verify ownership of source account
        if src_acc["owner_id"] != u_id:
            raise PermissionError(
                f"User '{u_id}' does not own source account '{source_account}'."
            )

        # 5. Validate transfer amount and funds
        _validate_funds(src_acc, money)

        # 6. Perform the transfer atomically
        src_acc["balance"] -= money
        dst_acc["balance"] += money

    # 7. Return success message
    return (
        f"Transfer of {money:.2f} from '{source_account}' to "
        f"'{destination_account}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        result = move_funds(
            u_id="U001",
            u_role="account_owner",
            source_account="ACC1001",
            destination_account="ACC1002",
            money=200.0,
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")