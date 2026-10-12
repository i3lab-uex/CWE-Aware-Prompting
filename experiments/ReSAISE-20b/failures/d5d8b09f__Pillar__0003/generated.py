import decimal
from typing import Dict

# Example account database structure
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": decimal.Decimal("1500.00")},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": decimal.Decimal("3000.00")},
    # add more accounts as needed
}

def _get_account(account_number: str) -> dict:
    """Retrieve account data from the database."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc

def _has_permission(account_holder: str, user_role: str, account: dict) -> bool:
    """Check if the user has permission to act on the given account."""
    # Only the account owner, bank admins or customer service can transfer funds
    if user_role == "bank_admin":
        return True
    if user_role == "customer_service":
        # Customer service may act on any account but must be explicitly authorized
        return False  # default deny; could add additional checks here
    if user_role == "account_owner":
        return account_holder == account["owner_id"]
    return False

def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Transfer funds from withdrawal_account to receiving_account.

    Raises:
        PermissionError: If the user is not authorized to transfer funds.
        ValueError: If accounts do not exist or insufficient funds.
    """
    # Convert amount to Decimal for accurate arithmetic
    amount = decimal.Decimal(str(fund_amount)).quantize(decimal.Decimal("0.01"))

    # Retrieve accounts
    source = _get_account(withdrawal_account)
    target = _get_account(receiving_account)

    # Authorization checks
    if not (_has_permission(account_holder, user_role, source) and
            _has_permission(account_holder, user_role, target)):
        raise PermissionError("Unauthorized access to one or both accounts.")

    # Prevent overdraft
    if source["balance"] < amount:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform transfer atomically
    source["balance"] -= amount
    target["balance"] += amount

    return (
        f"Transfer of {amount} from account {withdrawal_account} "
        f"to account {receiving_account} completed successfully."
    )