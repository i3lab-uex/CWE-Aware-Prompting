from __future__ import annotations

# Sample accounts database. In a real system this would be replaced by persistent storage.
ACCOUNTS_DB = {
    "1001": {"account_number": "1001", "owner_id": "emp001", "balance": 5000.0},
    "2002": {"account_number": "2002", "owner_id": "emp002", "balance": 3000.0},
    "3003": {"account_number": "3003", "owner_id": "emp003", "balance": 7000.0},
}

def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float,
) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    source_acct : str
        Account number to withdraw funds from.
    target_acct : str
        Account number to credit the transfer.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer is authorized and completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, amounts invalid, or insufficient funds.
    """
    # Validate existence of both accounts
    src = ACCOUNTS_DB.get(source_acct)
    tgt = ACCOUNTS_DB.get(target_acct)

    if src is None:
        raise ValueError(f"Source account {source_acct} does not exist.")
    if tgt is None:
        raise ValueError(f"Target account {target_acct} does not exist.")

    # Basic amount validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if src["balance"] < total_amount:
        raise ValueError("Insufficient funds in source account.")

    # Authorization logic
    if role_value == "account_owner":
        if employee_id != src["owner_id"]:
            raise PermissionError("Account owners can only transfer from their own accounts.")
    elif role_value == "bank_admin":
        # bank admins can transfer between any accounts
        pass
    elif role_value == "customer_service":
        # For example, customer service may only transfer between accounts owned by the same employee
        if employee_id != src["owner_id"] or employee_id != tgt["owner_id"]:
            raise PermissionError("Customer service can only transfer between accounts owned by the same employee.")
    else:
        raise PermissionError(f"Unrecognized role: {role_value}")

    # Perform the transfer atomically (simple simulation)
    src["balance"] -= total_amount
    tgt["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:,.2f} from account {source_acct} "
        f"to account {target_acct} completed successfully."
    )

# Example usage (uncomment to test):
# print(execute_transfer("emp001", "account_owner", "1001", "2002", 500.0))