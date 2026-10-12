# -*- coding: utf-8 -*-
"""
Banking transfer module.

This module defines a single function `move_money` that moves funds from one
account to another while enforcing proper access control.  It follows the
CWE‑284 (Improper Access Control) guidelines by ensuring that only an account
owner or a privileged role may perform the transfer.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  In‑memory account database (example structure)
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 1200.50},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 500.00},
    # Add more accounts as needed
}

# --------------------------------------------------------------------------- #
#  Role hierarchy (for quick lookup)
# --------------------------------------------------------------------------- #
AUTHORIZED_ROLES = {"bank_admin", "customer_service"}


def _get_account(account_number: str) -> dict:
    """
    Retrieve an account from the database.

    Parameters
    ----------
    account_number : str
        The account number to look up.

    Returns
    -------
    dict
        The account dictionary if found.

    Raises
    ------
    KeyError
        If the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account '{account_number}' not found.") from exc


def _has_permission(
    person_id: str,
    role: str,
    source_account: dict,
) -> bool:
    """
    Determine whether the caller is allowed to transfer from `source_account`.

    Parameters
    ----------
    person_id : str
        The ID of the user initiating the transfer.
    role : str
        The role of the user (e.g., 'account_owner', 'bank_admin').
    source_account : dict
        The source account dictionary.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # Account owner can transfer from their own account
    if role == "account_owner" and source_account["owner_id"] == person_id:
        return True

    # Bank admins and customer service can transfer any account
    if role in AUTHORIZED_ROLES:
        return True

    return False


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
        User ID initiating the transaction.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin').
    source_account : str
        Account number to withdraw from.
    destination_account : str
        Account number to deposit into.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the amount transferred and new balances.

    Raises
    ------
    PermissionError
        If the user is not authorized to transfer from the source account.
    ValueError
        If the transfer amount is invalid (negative or exceeds balance).
    KeyError
        If either account number does not exist.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src_acc = _get_account(source_account)
    dst_acc = _get_account(destination_account)

    # Enforce access control
    if not _has_permission(person_id, role, src_acc):
        raise PermissionError(
            f"User '{person_id}' with role '{role}' is not authorized to transfer from account {source_account}."
        )

    # Ensure sufficient funds
    if src_acc["balance"] < transfer_amount:
        raise ValueError(
            f"Insufficient funds in account {source_account}. "
            f"Available: {src_acc['balance']:.2f}, requested: {transfer_amount:.2f}."
        )

    # Perform transfer atomically (simple example; no real transaction support)
    src_acc["balance"] -= transfer_amount
    dst_acc["balance"] += transfer_amount

    return (
        f"Successfully transferred ${transfer_amount:.2f} from {source_account} "
        f"(new balance: ${src_acc['balance']:.2f}) to {destination_account} "
        f"(new balance: ${dst_acc['balance']:.2f})."
    )


# --------------------------------------------------------------------------- #
#  Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = move_money(
            person_id="user_001",
            role="account_owner",
            source_account="ACC1001",
            destination_account="ACC1002",
            transfer_amount=200.0,
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")