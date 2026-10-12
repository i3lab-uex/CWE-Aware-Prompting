import datetime

# Example account database (account_number -> account details)
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "EMP001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "EMP002", "balance": 3000.00},
    # Add more accounts as needed
}

def _get_account(acct_num: str) -> dict:
    """
    Retrieve account details from the database.
    Raises KeyError if the account does not exist.
    """
    return ACCOUNTS_DB[acct_num]

def _is_authorized(employee_id: str, role_value: str,
                   source_acct: dict, target_acct: dict) -> bool:
    """
    Determine whether the employee is authorized to perform the transfer.
    - bank_admin and customer_service can transfer any accounts.
    - account_owner can only transfer from their own account.
    """
    if role_value in {"bank_admin", "customer_service"}:
        return True
    if role_value == "account_owner":
        return employee_id == source_acct["owner_id"]
    # Unknown role is not authorized
    return False

def execute_transfer(employee_id: str,
                     role_value: str,
                     source_acct: str,
                     target_acct: str,
                     total_amount: float) -> str:
    """
    Transfer funds between two accounts with authorization checks.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acct : str
        Account number to withdraw from.
    target_acct : str
        Account number to deposit into.
    total_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    KeyError
        If either account does not exist in the database.
    ValueError
        If there are insufficient funds or if total_amount is non‑positive.
    """
    # Basic input validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    try:
        src_acct = _get_account(source_acct)
        tgt_acct = _get_account(target_acct)
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}")

    # Authorization check
    if not _is_authorized(employee_id, role_value, src_acct, tgt_acct):
        raise PermissionError(
            f"Employee '{employee_id}' with role '{role_value}' is not authorized "
            "to transfer from account '{}'.".format(source_acct)
        )

    # Funds check
    if src_acct["balance"] < total_amount:
        raise ValueError(
            f"Insufficient funds in source account '{source_acct}'. "
            f"Available: {src_acct['balance']}, required: {total_amount}."
        )

    # Perform the transfer atomically
    src_acct["balance"] -= total_amount
    tgt_acct["balance"] += total_amount

    # Optional: log the transaction (simplified)
    _log_transaction(employee_id, source_acct, target_acct, total_amount)

    return (
        f"Transfer of {total_amount:.2f} from '{source_acct}' to "
        f"'{target_acct}' completed successfully on {datetime.datetime.now():%Y-%m-%d %H:%M:%S}."
    )

def _log_transaction(employee_id: str, src_acct: str,
                     tgt_acct: str, amount: float) -> None:
    """
    Simple logging of the transaction. In a real system this would
    write to a secure audit log.
    """
    print(
        f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] "
        f"Employee '{employee_id}' transferred {amount:.2f} from '{src_acct}' "
        f"to '{tgt_acct}'."
    )