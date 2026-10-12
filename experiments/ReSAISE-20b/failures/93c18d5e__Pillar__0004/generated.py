#!/usr/bin/env python3
"""
Banking fund transfer module.

Implements a secure transfer function that enforces proper access control
(CWE‑284) and validates input before modifying account balances.
"""

from __future__ import annotations

import typing as _t
from decimal import Decimal, InvalidOperation

# Example in‑memory database. In a real system this would be replaced
# by persistent storage and proper authentication/authorization layers.
ACCOUNTS_DB: dict[str, dict[str, _t.Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": Decimal("5000.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": Decimal("3000.00")},
    # Add more accounts as needed
}

# Roles that are allowed to perform transfers
ALLOWED_ROLES = {"bank_admin", "customer_service"}


def _get_account(account_number: str) -> dict[str, _t.Any]:
    """Retrieve an account from the database or raise KeyError."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number!r} does not exist.") from exc


def _authorize(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: dict[str, _t.Any],
) -> None:
    """
    Check if the initiator is authorized to withdraw from the given account.
    Raises PermissionError on failure.
    """
    # Owner check
    if withdraw_account["owner_id"] == initiator_id:
        return

    # Role based check
    if initiator_role in ALLOWED_ROLES:
        return

    raise PermissionError(
        f"User {initiator_id!r} with role {initiator_role!r} is not authorized "
        f"to transfer from account {withdraw_account['account_number']!r}."
    )


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: _t.Union[float, Decimal],
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transaction.
    initiator_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdraw_account : str
        Account number to withdraw funds from.
    deposit_account : str
        Account number to deposit funds into.
    transfer_value : float | Decimal
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, negative amounts, or insufficient funds.
    """

    # Validate transfer amount
    try:
        amount = Decimal(str(transfer_value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Transfer value {transfer_value!r} is not a valid number.") from exc

    if amount <= 0:
        raise ValueError("Transfer value must be greater than zero.")

    # Retrieve accounts
    src = _get_account(withdraw_account)
    dst = _get_account(deposit_account)

    # Authorization check
    _authorize(initiator_id, initiator_role, src)

    # Balance checks
    if src["balance"] < amount:
        raise ValueError(
            f"Insufficient funds in account {src['account_number']}. "
            f"Available: {src['balance']}, Requested: {amount}"
        )

    # Perform transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account {src['account_number']} "
        f"to {dst['account_number']} completed successfully."
    )


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        msg = shift_funds(
            initiator_id="user123",
            initiator_role="account_owner",
            withdraw_account="ACC1001",
            deposit_account="ACC1002",
            transfer_value=250.75,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")