#!/usr/bin/env python3
"""
A simple in‑memory account transfer module that demonstrates correct authorization checks.
The code protects against CWE-863 (Incorrect Authorization) by verifying the role of
the user and ensuring that only owners or privileged roles can initiate a transfer.
"""

from __future__ import annotations

import decimal
from typing import Dict, Any

# Configure Decimal for accurate monetary calculations.
decimal.getcontext().prec = 28
Decimal = decimal.Decimal

# --------------------------------------------------------------------------- #
# Sample account database. In a real system this would be replaced by a
# persistent datastore with proper authentication/authorization layers.
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": Decimal("1500.00")},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_456", "balance": Decimal("2500.00")},
    "ACC3003": {"account_number": "ACC3003", "owner_id": "user_123", "balance": Decimal("500.00")},
}

# --------------------------------------------------------------------------- #
# Authorization helper
# --------------------------------------------------------------------------- #
def _is_authorized(u_identifier: str, u_role: str, account_from: str) -> bool:
    """
    Determine if the user is allowed to transfer funds from `account_from`.

    * The account owner can transfer funds from their own account.
    * A 'bank_admin' or 'customer_service' role can transfer funds from any account
      but only if the account exists.
    """
    # Normalise role to lowercase for case‑insensitive comparison
    role = u_role.lower()

    # Check that the source account exists
    if account_from not in ACCOUNTS_DB:
        return False

    # Owner check
    if role == "account_owner" and ACCOUNTS_DB[account_from]["owner_id"] == u_identifier:
        return True

    # Privileged roles
    if role in {"bank_admin", "customer_service"}:
        return True

    # All other cases are not allowed
    return False


# --------------------------------------------------------------------------- #
# Main transfer function
# --------------------------------------------------------------------------- #
def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer `transfer_amount` from `account_from` to `account_to`.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user making the request.
    u_role : str
        Role of the requesting user. Expected values:
            * 'account_owner'
            * 'bank_admin'
            * 'customer_service'
    account_from : str
        Source account number.
    account_to : str
        Destination account number.
    transfer_amount : float
        Amount to transfer. Must be positive.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid input such as negative amount or non‑existent accounts.
    """
    # Validate transfer amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure accounts exist
    if account_from not in ACCOUNTS_DB:
        raise ValueError(f"Source account '{account_from}' does not exist.")
    if account_to not in ACCOUNTS_DB:
        raise ValueError(f"Destination account '{account_to}' does not exist.")

    # Authorization check
    if not _is_authorized(u_identifier, u_role, account_from):
        raise PermissionError(
            f"User '{u_identifier}' with role '{u_role}' is not authorized to transfer from account '{account_from}'."
        )

    # Perform the transfer atomically
    amount = Decimal(str(transfer_amount))

    source_balance = ACCOUNTS_DB[account_from]["balance"]
    if source_balance < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Update balances
    ACCOUNTS_DB[account_from]["balance"] = source_balance - amount
    ACCOUNTS_DB[account_to]["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account '{account_from}' "
        f"to account '{account_to}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = fund_transfer(
            u_identifier="user_123",
            u_role="account_owner",
            account_from="ACC1001",
            account_to="ACC2002",
            transfer_amount=200.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")