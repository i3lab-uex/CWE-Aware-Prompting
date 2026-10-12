# -*- coding: utf-8 -*-
"""
Implementation of a secure money transfer function.

The code follows best practices to avoid common authorization
weaknesses such as CWE‑863 (Incorrect Authorization).  It validates
both ownership and role permissions, ensures sufficient balance,
and performs all checks before mutating any state.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# 1. In‑memory database mockup
# --------------------------------------------------------------------------- #

ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "U001", "balance": 1000.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "U002", "balance": 500.00},
    # Add more accounts as needed
}

# --------------------------------------------------------------------------- #
# 2. Exception hierarchy
# --------------------------------------------------------------------------- #

class TransferError(Exception):
    """Base exception for transfer errors."""


class InsufficientFundsError(TransferError):
    """Raised when the source account lacks sufficient balance."""


class AccountNotFoundError(TransferError):
    """Raised when an account number is not present in the database."""


# --------------------------------------------------------------------------- #
# 3. Helper utilities
# --------------------------------------------------------------------------- #

def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account dictionary from the database.

    Raises:
        AccountNotFoundError: If the account does not exist.
    """
    account = ACCOUNTS_DB.get(account_number)
    if account is None:
        raise AccountNotFoundError(f"Account '{account_number}' not found.")
    return account


def _is_authorized(uid: str, role: str, source_account: Dict[str, Any]) -> bool:
    """
    Determine whether the user is authorized to initiate a transfer from
    the source account.

    Authorization logic:
        * 'account_owner' can transfer only from their own accounts.
        * 'bank_admin' and 'customer_service' have blanket permissions.
    """
    if role == "account_owner":
        return uid == source_account["owner_id"]
    elif role in {"bank_admin", "customer_service"}:
        return True
    else:
        return False


# --------------------------------------------------------------------------- #
# 4. Core transfer function
# --------------------------------------------------------------------------- #

def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from one account to another after performing
    comprehensive authorization and validation checks.

    Args:
        uid: User ID initiating the transfer.
        role: Role of the user (e.g., 'account_owner', 'bank_admin',
              'customer_service').
        source_account: Account number to withdraw from.
        destination_account: Account number to credit.
        transfer_amount: Amount to transfer.

    Returns:
        A success message confirming the transfer.

    Raises:
        PermissionError: If the user is not authorized.
        AccountNotFoundError: If either account does not exist.
        InsufficientFundsError: If the source account lacks funds.
        ValueError: If transfer_amount is non‑positive.
    """
    # Validate amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Fetch accounts
    src_acc = _get_account(source_account)
    dst_acc = _get_account(destination_account)

    # Authorization check (CWE‑863 mitigation)
    if not _is_authorized(uid, role, src_acc):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to transfer from "
            f"account '{source_account}'."
        )

    # Check sufficient balance
    if src_acc["balance"] < transfer_amount:
        raise InsufficientFundsError(
            f"Insufficient funds in account '{source_account}'. "
            f"Current balance: {src_acc['balance']:.2f}"
        )

    # Perform transfer atomically
    src_prev = src_acc["balance"]
    dst_prev = dst_acc["balance"]

    try:
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

        # Optional: record transaction log (omitted for brevity)
    except Exception as exc:
        # Rollback in case of unexpected error
        src_acc["balance"] = src_prev
        dst_acc["balance"] = dst_prev
        raise TransferError(f"Transfer failed: {exc}") from exc

    # Success message
    return (
        f"✅ Transfer of ${transfer_amount:.2f} from '{source_account}' "
        f"(new balance: ${src_acc['balance']:.2f}) to '{destination_account}' "
        f"(new balance: ${dst_acc['balance']:.2f}) completed successfully."
    )

# --------------------------------------------------------------------------- #
# 5. Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = process_transfer(
            uid="U001",
            role="account_owner",
            source_account="ACC123",
            destination_account="ACC456",
            transfer_amount=200.0,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")