import decimal
from typing import Dict

# Sample in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": decimal.Decimal("1500.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": decimal.Decimal("500.00")},
    # Add more accounts as needed
}

def _get_account(account_number: str) -> Dict:
    """Retrieve account data from the database."""
    acct = ACCOUNTS_DB.get(account_number)
    if not acct:
        raise KeyError(f"Account {account_number} does not exist.")
    return acct

def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message upon successful transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        If fund_amount is non‑positive or other validation fails.
    KeyError
        If either account does not exist in the database.
    """

    # Basic validation
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Convert to Decimal for accurate arithmetic
    amount = decimal.Decimal(str(fund_amount))

    # Fetch accounts
    withdraw_acct = _get_account(withdrawal_account)
    receive_acct = _get_account(receiving_account)

    # Authorization check
    authorized = False
    if user_role == "bank_admin":
        authorized = True  # Admin can transfer any funds
    elif user_role == "account_owner" and account_holder == withdraw_acct["owner_id"]:
        authorized = True  # Owner of the withdrawal account
    elif user_role == "customer_service":
        # Example: customer service can transfer only if both accounts belong to the same user
        authorized = account_holder == withdraw_acct["owner_id"] and account_holder == receive_acct["owner_id"]

    if not authorized:
        raise PermissionError("Unauthorized access to transfer funds.")

    # Sufficient balance check
    if withdraw_acct["balance"] < amount:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform transfer atomically
    withdraw_acct["balance"] -= amount
    receive_acct["balance"] += amount

    return (
        f"Transfer of {amount} from account {withdrawal_account} "
        f"to account {receiving_account} completed successfully."
    )