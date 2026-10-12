#!/usr/bin/env python3
"""
execute_transfer: Safely transfer funds between two accounts.

The function verifies that the employee initiating the transfer
has appropriate authorization and that the source account has enough
balance before performing the debit/credit.  All operations are
performed atomically to avoid race conditions.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# ----------------------------------------------------------------------
# Mock database of accounts.
# In a real system this would be replaced with persistent storage
# and proper concurrency control (e.g., database transactions).
# ----------------------------------------------------------------------
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.00},
    # Add more accounts as needed.
}

# ----------------------------------------------------------------------
# Lock dictionary to ensure thread‑safe updates per account
# ----------------------------------------------------------------------
_account_locks: Dict[str, threading.Lock] = {
    acct_no: threading.Lock() for acct_no in ACCOUNTS_DB
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_account(acct_no: str) -> Dict[str, Any]:
    """Retrieve account data; raise KeyError if not found."""
    try:
        return ACCOUNTS_DB[acct_no]
    except KeyError as exc:
        raise ValueError(f"Account {acct_no} does not exist.") from exc


def _has_permission(employee_id: str, role_value: str,
                    source_acct_owner: str) -> bool:
    """
    Determine if the employee is authorized to transfer from source_acct.
    Allowed roles:
      - account_owner: must be the owner of the source account
      - bank_admin: has unrestricted access
      - customer_service: may transfer only if explicitly allowed (not implemented here)
    """
    if role_value == "bank_admin":
        return True
    if role_value == "account_owner" and employee_id == source_acct_owner:
        return True
    # Additional role checks (e.g., customer_service) can be added here.
    return False


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def execute_transfer(employee_id: str,
                     role_value: str,
                     source_acct: str,
                     target_acct: str,
                     total_amount: float) -> str:
    """
    Transfer `total_amount` from `source_acct` to `target_acct`.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the employee (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acct : str
        Account number to debit.
    target_acct : str
        Account number to credit.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating completion of the transfer.

    Raises
    ------
    PermissionError
        If the employee is not authorized to perform this transfer.
    ValueError
        For invalid accounts, insufficient funds, or negative amounts.
    """
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve account data
    src = _get_account(source_acct)
    tgt = _get_account(target_acct)

    # Authorization check
    if not _has_permission(employee_id, role_value, src["owner_id"]):
        raise PermissionError(
            f"Employee {employee_id} with role '{role_value}' "
            "is not authorized to transfer from account "
            f"{source_acct}."
        )

    # Acquire locks for both accounts in a consistent order to avoid deadlocks
    first, second = (
        (source_acct, target_acct)
        if source_acct < target_acct
        else (target_acct, source_acct)
    )
    with _account_locks[first], _account_locks[second]:
        # Re‑validate balance after acquiring lock
        if src["balance"] < total_amount:
            raise ValueError(
                f"Insufficient funds in account {source_acct}. "
                f"Available: {src['balance']:.2f}, required: {total_amount:.2f}."
            )

        # Perform transfer
        src["balance"] -= total_amount
        tgt["balance"] += total_amount

    return (
        f"Transfer of {total_amount:.2f} from account "
        f"{source_acct} to account {target_acct} completed successfully."
    )


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        msg = execute_transfer(
            employee_id="user_001",
            role_value="account_owner",
            source_acct="ACC1001",
            target_acct="ACC1002",
            total_amount=1500.00,
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")