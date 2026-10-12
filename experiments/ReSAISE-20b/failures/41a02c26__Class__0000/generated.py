#!/usr/bin/env python3
"""
Bank transfer helper.

The function ``process_transfer`` moves money from a source account to a destination
account after performing strict authorization checks.  It follows the principle of
least privilege and protects against CWE‑863 (Incorrect Authorization).

The module contains only what is needed for the transfer logic.  No external
packages are required beyond the standard library.
"""

from __future__ import annotations

import decimal
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock database of accounts.  In a real system this would be replaced with
# persistent storage (e.g., a relational database or an ORM).
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    # Example accounts
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": decimal.Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": decimal.Decimal("500.00")},
    # Add more accounts as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _get_account(account_number: str) -> Dict[str, Any]:
    """Retrieve an account from the database.

    Raises:
        KeyError: If the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account '{account_number}' not found.") from exc


def _is_authorized(uid: str, role: str, source_account: Dict[str, Any]) -> bool:
    """Check whether the user is allowed to initiate a transfer from the source account.

    Authorization logic:
        * The user must be the owner of the source account.
        * OR the user has a privileged role (e.g., 'bank_admin', 'customer_service').
    """
    if uid == source_account["owner_id"]:
        return True
    if role in {"bank_admin", "customer_service"}:
        return True
    return False


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def process_transfer(
    uid: str,
    role: str,
    source_account_number: str,
    destination_account_number: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts.

    Args:
        uid: User ID initiating the transfer.
        role: Role of the user ('account_owner', 'bank_admin', etc.).
        source_account_number: Account number to withdraw from.
        destination_account_number: Target account number.
        transfer_amount: Amount to transfer (must be positive).

    Returns:
        A success message confirming the transfer.

    Raises:
        PermissionError: If the user is not authorized to transfer from the source.
        ValueError: For invalid amounts or non‑existent accounts.
    """
    # Normalise transfer amount
    try:
        amount = decimal.Decimal(str(transfer_amount))
    except decimal.InvalidOperation as exc:
        raise ValueError("Transfer amount must be a numeric value.") from exc

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    # Fetch accounts
    source_acc = _get_account(source_account_number)
    dest_acc = _get_account(destination_account_number)

    # Authorization check
    if not _is_authorized(uid, role, source_acc):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to transfer from account {source_account_number}."
        )

    # Sufficient funds check
    if source_acc["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    source_acc["balance"] -= amount
    dest_acc["balance"] += amount

    # Return confirmation
    return (
        f"Transfer of {amount:.2f} from account '{source_account_number}' "
        f"to account '{destination_account_number}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = process_transfer(
            uid="user_1",
            role="account_owner",
            source_account_number="ACC001",
            destination_account_number="ACC002",
            transfer_amount=150.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")