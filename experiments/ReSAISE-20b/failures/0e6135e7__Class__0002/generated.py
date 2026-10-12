# -*- coding: utf-8 -*-
"""
A minimal financial transfer module that demonstrates correct authorization checks.
"""

from __future__ import annotations

import decimal
from typing import Dict

# --------------------------------------------------------------------------- #
# Sample in‑memory accounts database
# --------------------------------------------------------------------------- #

ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": decimal.Decimal("1500.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": decimal.Decimal("3000.00")},
    # Add more accounts as needed
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class InsufficientFundsError(Exception):
    """Raised when an account does not have enough balance to complete the transfer."""
    pass


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float
) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    identifier : str
        The user ID performing the transfer.
    role : str
        Role of the requester. Allowed values are:
            - 'account_owner'
            - 'bank_admin'
            - 'customer_service'
    source_acc : str
        Source account number.
    destination_acc : str
        Destination account number.
    value : float
        Amount to transfer (must be positive).

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the requester does not have permission to perform this transfer.
    ValueError
        If input validation fails (negative value, unknown account, etc.).
    InsufficientFundsError
        If the source account lacks sufficient funds.
    """

    # --------------------------------------------------------------------- #
    # Input validation
    # --------------------------------------------------------------------- #

    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Convert to Decimal for accurate arithmetic
    transfer_amount = decimal.Decimal(str(value))

    if source_acc not in ACCOUNTS_DB:
        raise ValueError(f"Source account '{source_acc}' does not exist.")
    if destination_acc not in ACCOUNTS_DB:
        raise ValueError(f"Destination account '{destination_acc}' does not exist.")

    source = ACCOUNTS_DB[source_acc]
    destination = ACCOUNTS_DB[destination_acc]

    # --------------------------------------------------------------------- #
    # Authorization check (CWE-863 protection)
    # --------------------------------------------------------------------- #

    # Account owners may only transfer from their own accounts
    if role == "account_owner":
        if source["owner_id"] != identifier:
            raise PermissionError("Account owners can only transfer from their own accounts.")
        # Optionally, prevent transferring to the same account
        if source_acc == destination_acc:
            raise ValueError("Source and destination accounts must differ.")
    # Bank admins and customer service have full privileges
    elif role in ("bank_admin", "customer_service"):
        # No further checks needed for these roles
        pass
    else:
        raise PermissionError(f"Role '{role}' is not authorized to perform transfers.")

    # --------------------------------------------------------------------- #
    # Balance check
    # --------------------------------------------------------------------- #

    if source["balance"] < transfer_amount:
        raise InsufficientFundsError("Insufficient funds in the source account.")

    # --------------------------------------------------------------------- #
    # Perform transfer atomically (in this simple example we just update dicts)
    # --------------------------------------------------------------------- #

    source["balance"] -= transfer_amount
    destination["balance"] += transfer_amount

    # --------------------------------------------------------------------- #
    # Return success message
    # --------------------------------------------------------------------- #

    return (
        f"Transfer of {transfer_amount:.2f} from account '{source_acc}' "
        f"to account '{destination_acc}' completed successfully."
    )

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = execute_transfer(
            identifier="user123",
            role="account_owner",
            source_acc="ACC1001",
            destination_acc="ACC1002",
            value=200.0
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")