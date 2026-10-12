# ──────────────────────────────────────────────────────────────
# Banking transfer module
# ──────────────────────────────────────────────────────────────

from typing import Dict, Any

# Sample in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": 2000.00},
    # Add more accounts as needed
}


class InsufficientFundsError(Exception):
    """Raised when an account does not have enough balance for the transfer."""
    pass


def _is_authorized(person_id: str, role: str,
                   source_account: str, destination_account: str) -> bool:
    """
    Determine if the user is allowed to perform a transfer between the
    specified accounts.

    Authorization logic:
      * Bank admins and customer service can transfer any funds.
      * Account owners can only move money from accounts they own.
    """
    if role in {"bank_admin", "customer_service"}:
        return True

    # Account owner must own the source account
    src_acc = ACCOUNTS_DB.get(source_account)
    if not src_acc:
        return False
    return src_acc["owner_id"] == person_id


def move_money(person_id: str,
               role: str,
               source_account: str,
               destination_account: str,
               transfer_amount: float) -> str:
    """
    Move money from `source_account` to `destination_account`.

    Parameters
    ----------
    person_id : str
        Identifier of the user initiating the transfer.
    role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer completes.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    InsufficientFundsError
        If the source account does not have enough balance.
    KeyError
        If either account number is unknown.
    ValueError
        If transfer_amount <= 0 or accounts are identical.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if source_account == destination_account:
        raise ValueError("Source and destination accounts must differ.")

    # Ensure both accounts exist
    src_acc = ACCOUNTS_DB[source_account]
    dst_acc = ACCOUNTS_DB[destination_account]

    # Authorization check
    if not _is_authorized(person_id, role, source_account, destination_account):
        raise PermissionError("Unauthorized access: insufficient permissions to transfer funds.")

    # Check sufficient balance
    if src_acc["balance"] < transfer_amount:
        raise InsufficientFundsError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src_acc["balance"] -= transfer_amount
    dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:,.2f} from {source_account}"
        f" to {destination_account} completed successfully."
    )