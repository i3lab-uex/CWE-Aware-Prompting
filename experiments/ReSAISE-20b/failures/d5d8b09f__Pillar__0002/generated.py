from decimal import Decimal, InvalidOperation
from typing import Dict

# Sample in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}


def _get_account(account_number: str) -> Dict:
    """Retrieve an account from the database or raise KeyError."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account '{account_number}' does not exist.") from exc


def _authorize(
    account_holder: str,
    user_role: str,
    withdrawal_account: Dict,
) -> None:
    """
    Verify that the user is authorized to withdraw from the account.
    Raises PermissionError if unauthorized.
    """
    # Bank admins and customer service can transfer from any account
    if user_role in {"bank_admin", "customer_service"}:
        return

    # Account owner must match
    if withdrawal_account["owner_id"] != account_holder:
        raise PermissionError(
            "Unauthorized: Only the account owner or a privileged role may initiate transfers."
        )


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        or 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
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
        For invalid account numbers, insufficient funds, or negative amounts.
    """
    # Input validation and conversion
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    try:
        amount = Decimal(str(fund_amount))
    except InvalidOperation as exc:
        raise ValueError("Invalid transfer amount.") from exc

    # Retrieve accounts
    withdraw_acc = _get_account(withdrawal_account)
    receive_acc = _get_account(receiving_account)

    # Authorization check
    _authorize(account_holder, user_role, withdraw_acc)

    # Check sufficient funds
    if withdraw_acc["balance"] < amount:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform transfer atomically
    withdraw_acc["balance"] -= amount
    receive_acc["balance"] += amount

    return (
        f"Success: {amount:.2f} transferred from "
        f"{withdrawal_account} to {receiving_account}."
    )