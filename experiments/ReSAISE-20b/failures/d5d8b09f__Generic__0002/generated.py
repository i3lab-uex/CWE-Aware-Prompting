# banking.py

ACCOUNTS_DB = {
    # Example structure:
    # "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    # Add actual account data here
}

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
        The user ID initiating the transaction.
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
        Success message if the transfer is authorized and completed.
    
    Raises
    ------
    PermissionError
        If the user does not have permission to perform this transfer.
    ValueError
        If accounts are missing, amounts invalid or insufficient balance.
    """
    # Validate input amount
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    withdrawal = ACCOUNTS_DB.get(withdrawal_account)
    receiving = ACCOUNTS_DB.get(receiving_account)

    if not withdrawal:
        raise ValueError(f"Withdrawal account '{withdrawal_account}' does not exist.")
    if not receiving:
        raise ValueError(f"Receiving account '{receiving_account}' does not exist.")

    # Authorization check
    if user_role == "account_owner":
        if withdrawal["owner_id"] != account_holder:
            raise PermissionError("Account owner can only transfer from their own accounts.")
    elif user_role in ("bank_admin", "customer_service"):
        # Admins and customer service can transfer any account
        pass
    else:
        raise PermissionError(f"User role '{user_role}' is not authorized to transfer funds.")

    # Sufficient balance check
    if withdrawal["balance"] < fund_amount:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform transfer atomically
    withdrawal["balance"] -= fund_amount
    receiving["balance"] += fund_amount

    return (
        f"Transfer of ${fund_amount:,.2f} from account "
        f"{withdrawal_account} to {receiving_account} completed successfully."
    )