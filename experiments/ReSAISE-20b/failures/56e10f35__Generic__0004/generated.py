from __future__ import annotations

import datetime
from typing import Dict, Any

# Sample in‑memory accounts database.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "U001", "balance": 1500.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "U002", "balance": 500.00},
    # Add more accounts as needed.
}


def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account from the database.
    Raises KeyError if the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account {account_number} not found.") from exc


def _authorize(initiator_id: str, position: str, account: Dict[str, Any]) -> bool:
    """
    Determine if the user is authorized to operate on the account.
    - 'account_owner' can operate only on their own accounts.
    - 'bank_admin' and 'customer_service' have full access.
    """
    if position == "bank_admin" or position == "customer_service":
        return True
    if position == "account_owner" and account["owner_id"] == initiator_id:
        return True
    return False


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer money from `withdraw_account` to `deposit_account`.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    withdraw_account : str
        Account number to withdraw funds from.
    deposit_account : str
        Target account number to receive funds.
    transfer_value : float
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
        If either account does not exist.
    ValueError
        If the transfer amount is non‑positive or insufficient funds.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    from_account = _get_account(withdraw_account)
    to_account = _get_account(deposit_account)

    # Authorization check
    if not (_authorize(initiator_id, position, from_account) and
            _authorize(initiator_id, position, to_account)):
        raise PermissionError("User not authorized for this transfer.")

    # Balance check
    if from_account["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdraw account.")

    # Perform atomic transfer
    from_account["balance"] -= transfer_value
    to_account["balance"] += transfer_value

    # Optional: record transaction (omitted for brevity)
    timestamp = datetime.datetime.utcnow().isoformat()
    message = (
        f"Transfer of ${transfer_value:,.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully at {timestamp}."
    )
    return message