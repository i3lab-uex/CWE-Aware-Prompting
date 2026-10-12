#!/usr/bin/env python3
"""
A simple in‑memory account transfer system with proper authorization checks.

The module defines a single public function, `move_funds`, that moves money
between accounts in the global `ACCOUNTS_DB`.  It performs strict validation
and raises a PermissionError when the caller does not have sufficient rights.
"""

from __future__ import annotations

import decimal
from dataclasses import dataclass, field
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Configuration and data structures
# --------------------------------------------------------------------------- #

@dataclass
class Account:
    """Represents a bank account."""
    account_number: str
    owner_id: str
    balance: decimal.Decimal = field(default_factory=lambda: decimal.Decimal("0.00"))

# Global in‑memory database of accounts indexed by account number
ACCOUNTS_DB: Dict[str, Account] = {
    "ACC1001": Account(account_number="ACC1001", owner_id="user_001", balance=decimal.Decimal("1500.00")),
    "ACC1002": Account(account_number="ACC1002", owner_id="user_002", balance=decimal.Decimal("2500.00")),
    "ACC1003": Account(account_number="ACC1003", owner_id="user_003", balance=decimal.Decimal("500.00")),
}

# Define roles that can perform any transfer
ADMIN_ROLES = {"bank_admin", "customer_service"}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_account(account_number: str) -> Optional[Account]:
    """Retrieve an account from the database, or None if it does not exist."""
    return ACCOUNTS_DB.get(account_number)


def _is_authorized(u_id: str, u_role: str, source: Account) -> bool:
    """
    Determine whether the user is authorized to move funds from `source`.

    Rules:
      * The account owner may transfer money from their own account.
      * Admin roles (bank_admin, customer_service) may transfer from any account.
    """
    if u_role in ADMIN_ROLES:
        return True
    return source.owner_id == u_id


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float
) -> str:
    """
    Transfer `money` from `source_account` to `destination_account`.

    Parameters
    ----------
    u_id : str
        Identifier of the user requesting the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    money : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the caller is not authorized to perform this transfer.
    ValueError
        If accounts are missing, amounts are invalid or insufficient funds.
    """
    # Basic validation
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = _get_account(source_account)
    dst = _get_account(destination_account)

    if src is None:
        raise ValueError(f"Source account '{source_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{destination_account}' does not exist.")

    # Authorization check (CWE-863 mitigation)
    if not _is_authorized(u_id, u_role, src):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to transfer from account '{source_account}'."
        )

    # Ensure sufficient funds
    amount = decimal.Decimal(str(money)).quantize(decimal.Decimal("0.01"))
    if src.balance < amount:
        raise ValueError(
            f"Insufficient funds: source balance {src.balance} is less than transfer amount {amount}."
        )

    # Perform the transfer atomically
    src.balance -= amount
    dst.balance += amount

    return (
        f"Transfer of {amount} from '{source_account}' to "
        f"'{destination_account}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = move_funds(
            u_id="user_001",
            u_role="account_owner",
            source_account="ACC1001",
            destination_account="ACC1002",
            money=200.00,
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")