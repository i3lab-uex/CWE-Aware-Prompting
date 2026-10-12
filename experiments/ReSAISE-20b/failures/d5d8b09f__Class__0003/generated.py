import datetime

# Sample accounts database – in a real system this would be persisted securely.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 3000.00},
    # ... more accounts
}

def _is_authorized(user_id: str, role: str, from_account: dict) -> bool:
    """
    Internal helper to check if the user is allowed to transfer from the given account.
    - 'account_owner' must own the source account.
    - 'bank_admin' and 'customer_service' are privileged roles allowed to transfer from any account.
    """
    if role == "bank_admin" or role == "customer_service":
        return True
    if role == "account_owner" and from_account["owner_id"] == user_id:
        return True
    return False

def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Transfer funds between accounts with proper authorization and validation.
    
    Parameters
    ----------
    account_holder : str
        The ID of the user initiating the transaction.
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
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, negative amounts, or insufficient funds.
    """
    # Basic input validation
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts – ensure they exist
    src = ACCOUNTS_DB.get(withdrawal_account)
    dst = ACCOUNTS_DB.get(receiving_account)

    if src is None or dst is None:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization check (CWE-863 mitigated by strict comparison)
    if not _is_authorized(account_holder, user_role, src):
        raise PermissionError("User is not authorized to transfer from this account.")

    # Sufficient funds check
    if src["balance"] < fund_amount:
        raise ValueError("Insufficient balance in the withdrawal account.")

    # Perform transfer atomically
    src["balance"] -= fund_amount
    dst["balance"] += fund_amount

    # Record transaction (placeholder – in real life this would be logged securely)
    timestamp = datetime.datetime.utcnow().isoformat()
    # e.g., log_transaction(account_holder, withdrawal_account, receiving_account, fund_amount, timestamp)

    return (
        f"Transfer of ${fund_amount:,.2f} from {withdrawal_account} "
        f"to {receiving_account} completed successfully on {timestamp} UTC."
    )