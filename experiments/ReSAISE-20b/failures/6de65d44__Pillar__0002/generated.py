# -*- coding: utf-8 -*-

"""
Banking transfer module.

This module defines a `move_money` function that transfers funds between
accounts while enforcing proper access control.  It follows the
CWE‑284 (Improper Access Control) guidelines by ensuring that only users
with appropriate privileges can perform a transfer.
"""

from __future__ import annotations

# Sample in‑memory database. In production this would be replaced by a
# persistent store (e.g., SQL, NoSQL, or an ORM).
ACCOUNTS_DB: dict[str, dict] = {
    # account_number : { 'account_number': str, 'owner_id': str, 'balance': float }
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_456", "balance": 1200.50},
    # add more accounts as needed
}


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from `source_account` to `destination_account`.

    Parameters
    ----------
    person_id : str
        The ID of the user initiating the transaction.
    role : str
        Role of the user.  Valid values are:
            - 'account_owner': can transfer from accounts they own.
            - 'bank_admin' or 'customer_service': unrestricted access.
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
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist in `ACCOUNTS_DB`.
    ValueError
        If the transfer amount is non‑positive or insufficient funds.
    """
    # Validate accounts exist
    if source_account not in ACCOUNTS_DB:
        raise KeyError(f"Source account '{source_account}' does not exist.")
    if destination_account not in ACCOUNTS_DB:
        raise KeyError(f"Destination account '{destination_account}' does not exist.")

    src_acc = ACCOUNTS_DB[source_account]
    dst_acc = ACCOUNTS_DB[destination_account]

    # Authorization check
    if role == "account_owner":
        if src_acc["owner_id"] != person_id:
            raise PermissionError(
                "Unauthorized: account owner can only transfer from their own accounts."
            )
    elif role in {"bank_admin", "customer_service"}:
        # These roles are allowed to transfer from any account
        pass
    else:
        raise PermissionError(f"Unauthorized role: '{role}'.")

    # Validate transfer amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if src_acc["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform the transfer
    src_acc["balance"] -= transfer_amount
    dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from "
        f"{source_account} to {destination_account} completed successfully."
    )