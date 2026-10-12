#!/usr/bin/env python3
"""
A simple in‑memory account transfer module.

The implementation protects against CWE‑863 by performing a strict
authorization check before any balance modifications occur.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------


@dataclass
class Account:
    """Represents a bank account."""

    account_number: str
    owner_id: str
    balance: float = field(default=0.0)

    def deposit(self, amount: float) -> None:
        """Add money to the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Subtract money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount


# ----------------------------------------------------------------------
# In‑memory database
# ----------------------------------------------------------------------


ACCOUNTS_DB: Dict[str, Account] = {
    "ACC1001": Account(account_number="ACC1001", owner_id="USR001", balance=1500.00),
    "ACC2002": Account(account_number="ACC2002", owner_id="USR002", balance=500.00),
    "ACC3003": Account(account_number="ACC3003", owner_id="USR003", balance=750.00),
}

# ----------------------------------------------------------------------
# Authorization logic
# ----------------------------------------------------------------------


def _is_authorized(
    identifier: str, role: str, source_acc: Account
) -> bool:
    """
    Determine whether the requesting user is allowed to initiate a transfer
    from *source_acc*.

    - account_owner: must own the source account.
    - bank_admin or customer_service: allowed to transfer from any account.
    """
    if role == "account_owner":
        return source_acc.owner_id == identifier
    elif role in {"bank_admin", "customer_service"}:
        return True
    else:
        # Unknown role – deny access
        return False


# ----------------------------------------------------------------------
# Transfer function
# ----------------------------------------------------------------------


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float,
) -> str:
    """
    Transfer *value* from *source_acc* to *destination_acc*.

    Parameters
    ----------
    identifier : str
        ID of the user initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acc : str
        Account number to withdraw from.
    destination_acc : str
        Account number to deposit into.
    value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message with a timestamp.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account number does not exist in the database.
    ValueError
        For invalid amounts or insufficient funds.
    """
    # Input validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts from the database
    try:
        src_account = ACCOUNTS_DB[source_acc]
    except KeyError as exc:
        raise KeyError(f"Source account '{source_acc}' not found") from exc

    try:
        dst_account = ACCOUNTS_DB[destination_acc]
    except KeyError as exc:
        raise KeyError(f"Destination account '{destination_acc}' not found") from exc

    # Authorization check – must happen before any state changes
    if not _is_authorized(identifier, role, src_account):
        raise PermissionError(
            f"User '{identifier}' with role '{role}' is not authorized "
            f"to transfer from account '{source_acc}'."
        )

    # Perform the transfer atomically
    src_account.withdraw(value)
    dst_account.deposit(value)

    timestamp = datetime.datetime.utcnow().isoformat()
    return (
        f"Transfer of {value:.2f} from '{source_acc}' to "
        f"'{destination_acc}' completed successfully at {timestamp} UTC."
    )


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------


if __name__ == "__main__":
    try:
        msg = execute_transfer(
            identifier="USR001",
            role="account_owner",
            source_acc="ACC1001",
            destination_acc="ACC2002",
            value=200.0,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")