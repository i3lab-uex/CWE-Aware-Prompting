# -*- coding: utf-8 -*-
"""
Banking system – money transfer module.
"""

from typing import Dict

# Example in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_456", "balance": 3000.0},
    # Add more accounts as needed
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
        ID of the user initiating the transfer.
    role : str
        Role of the user. Valid values are:
            - 'account_owner'
            - 'bank_admin'
            - 'customer_service' (not allowed to perform transfers)
    source_account : str
        Account number from which funds are withdrawn.
    destination_account : str
        Account number to which funds are deposited.
    transfer_amount : float
        Amount of money to transfer. Must be positive.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid arguments such as non‑existent accounts, insufficient balance,
        or negative transfer amounts.
    """

    # Basic validation of arguments
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise ValueError(f"Source account '{source_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{destination_account}' does not exist.")

    # Authorization checks
    if role == "account_owner":
        if src["owner_id"] != person_id:
            raise PermissionError("Account owner can only transfer from their own account.")
    elif role == "bank_admin":
        # Bank admins have unrestricted access
        pass
    else:
        # Any other role is not permitted to perform transfers
        raise PermissionError(f"Role '{role}' is not authorized to transfer funds.")

    # Balance check
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from '{source_account}' "
        f"to '{destination_account}' completed successfully."
    )