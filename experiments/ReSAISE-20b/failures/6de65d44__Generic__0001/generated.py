#!/usr/bin/env python3
"""
A simple in‑memory banking module that supports transferring money between accounts.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock database of accounts.  In a real system this would be replaced by
# persistent storage (SQL, NoSQL, etc.).  For thread safety we guard all
# mutations with a global lock.
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "U456", "balance": 500.00},
    # Add more accounts as needed
}

# Global lock to protect concurrent modifications of ACCOUNTS_DB
_db_lock = threading.Lock()

# --------------------------------------------------------------------------- #
# Permissions
# --------------------------------------------------------------------------- #
ALLOWED_ROLES_FOR_TRANSFER = {"account_owner", "bank_admin", "customer_service"}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _get_account(account_number: str) -> Dict[str, Any]:
    """Return the account dictionary or raise KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc


def _is_authorized(person_id: str, role: str, source_account: Dict[str, Any]) -> bool:
    """
    Determine if the user is authorized to initiate a transfer.
    - bank_admin and customer_service are always allowed.
    - account_owner must own the source account.
    """
    if role not in ALLOWED_ROLES_FOR_TRANSFER:
        return False

    if role == "account_owner":
        return source_account["owner_id"] == person_id
    # bank_admin and customer_service have blanket permissions
    return True


# --------------------------------------------------------------------------- #
# Main API function
# --------------------------------------------------------------------------- #
def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    person_id : str
        ID of the user initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        or 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
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
        If any account does not exist, amounts are invalid,
        or insufficient funds.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:  # Ensure atomicity of the transfer
        src_acc = _get_account(source_account)
        dst_acc = _get_account(destination_account)

        # Authorization check
        if not _is_authorized(person_id, role, src_acc):
            raise PermissionError(
                f"User '{person_id}' with role '{role}' is not authorized to transfer from account {source_account}."
            )

        # Sufficient funds check
        if src_acc["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in source account {source_account}."
            )

        # Perform the transfer
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

    # Return a concise success message
    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )