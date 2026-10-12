# --------------------------------------------------------------
# Banking transfer module
# --------------------------------------------------------------

from __future__ import annotations
import threading
from typing import Dict, Any

# Example structure of the accounts database.
# In a real system this would be replaced by persistent storage
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    # account_number : { 'owner_id': str, 'balance': float }
}

# Lock to guard concurrent access to the accounts database
_ACCOUNTS_LOCK = threading.RLock()


def _is_authorized(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
) -> bool:
    """
    Determine if the initiator is allowed to transfer from the given account.
    """
    # Bank administrators can perform any transfer
    if initiator_role == "bank_admin":
        return True

    # Account owners can transfer only from their own account
    if initiator_role == "account_owner":
        account = ACCOUNTS_DB.get(withdraw_account)
        return account is not None and account["owner_id"] == initiator_id

    # Customer service agents are allowed to transfer only between accounts
    # belonging to the same customer (owner_id must match both)
    if initiator_role == "customer_service":
        account = ACCOUNTS_DB.get(withdraw_account)
        return (
            account is not None
            and account["owner_id"] == initiator_id  # service agent's own ID?
        )

    return False


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Move money from `withdraw_account` to `deposit_account`.

    Parameters
    ----------
    initiator_id : str
        User ID that initiates the transfer.
    initiator_role : str
        Role of the user (`account_owner`, `bank_admin`, or `customer_service`).
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform this transfer.
    ValueError
        If accounts are missing, balances insufficient, or amount is non‑positive.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive")

    with _ACCOUNTS_LOCK:
        # Validate accounts exist
        source = ACCOUNTS_DB.get(withdraw_account)
        target = ACCOUNTS_DB.get(deposit_account)

        if source is None:
            raise ValueError(f"Source account '{withdraw_account}' does not exist")
        if target is None:
            raise ValueError(f"Target account '{deposit_account}' does not exist")

        # Authorization check
        if not _is_authorized(initiator_id, initiator_role, withdraw_account):
            raise PermissionError(
                f"User '{initiator_id}' with role '{initiator_role}' "
                "is not authorized to transfer from account "
                f"'{withdraw_account}'."
            )

        # Check sufficient funds
        if source["balance"] < transfer_value:
            raise ValueError(
                f"Insufficient funds in account '{withdraw_account}'. "
                f"Available: {source['balance']:.2f}, required: {transfer_value:.2f}"
            )

        # Perform transfer
        source["balance"] -= transfer_value
        target["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from account '{withdraw_account}' "
        f"to account '{deposit_account}' completed successfully."
    )