from decimal import Decimal, InvalidOperation
from typing import Dict

# Sample in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.75},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 750.00},
    # ... other accounts
}


class BankError(Exception):
    """Base class for banking errors."""


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    withdrawal_account : str
        Account number to withdraw from.
    receiving_account : str
        Account number to deposit into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer is authorized and executed.

    Raises
    ------
    PermissionError
        If the user does not have permission to perform the transfer.
    BankError
        For invalid accounts, insufficient funds, or negative amounts.
    """

    # 1. Validate input amount
    try:
        amount = Decimal(str(fund_amount))
    except InvalidOperation:
        raise BankError("Invalid transfer amount.")

    if amount <= 0:
        raise BankError("Transfer amount must be positive.")

    # 2. Verify both accounts exist
    withdrawal = ACCOUNTS_DB.get(withdrawal_account)
    receiving = ACCOUNTS_DB.get(receiving_account)

    if withdrawal is None:
        raise BankError(f"Withdrawal account '{withdrawal_account}' does not exist.")
    if receiving is None:
        raise BankError(f"Receiving account '{receiving_account}' does not exist.")

    # 3. Authorization check (CWE‑863 protection)
    authorized = False
    if user_role == "account_owner":
        # Owner can only transfer from their own account.
        authorized = withdrawal["owner_id"] == account_holder
    elif user_role in {"bank_admin", "customer_service"}:
        # These roles have broader privileges but still must be present in the system.
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized access: insufficient privileges to transfer funds.")

    # 4. Check sufficient balance
    if Decimal(str(withdrawal["balance"])) < amount:
        raise BankError("Insufficient funds in the withdrawal account.")

    # 5. Perform transfer atomically (simple simulation)
    withdrawal["balance"] = float(Decimal(str(withdrawal["balance"])) - amount)
    receiving["balance"] = float(Decimal(str(receiving["balance"])) + amount)

    return (
        f"Transfer of {amount:.2f} from account '{withdrawal_account}' "
        f"to account '{receiving_account}' completed successfully."
    )