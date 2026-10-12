import threading

# Simulated in‑memory accounts database.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 5000.0},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 3000.0},
    # Add more accounts as needed.
}

# A simple lock to guard concurrent modifications of the accounts database.
_db_lock = threading.Lock()


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float,
) -> str:
    """
    Perform a transfer between two accounts if the caller is authorized.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_acct : str
        Account number from which funds will be withdrawn.
    target_acct : str
        Account number to which funds will be deposited.
    total_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating the transfer has been completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts do not exist or insufficient funds.
    """
    # Basic validation of inputs.
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts from the database.
    source = ACCOUNTS_DB.get(source_acct)
    target = ACCOUNTS_DB.get(target_acct)

    if source is None or target is None:
        raise ValueError("One or both account numbers are invalid")

    # Authorization logic.
    if role_value == "bank_admin" or role_value == "customer_service":
        # Admins and customer service can transfer between any accounts.
        authorized = True
    elif role_value == "account_owner":
        # Account owners may only transfer from accounts they own.
        authorized = source["owner_id"] == employee_id
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{employee_id}' with role '{role_value}' is not authorized "
            "to transfer from account '{}'".format(source_acct)
        )

    # Perform the transfer atomically.
    with _db_lock:
        if source["balance"] < total_amount:
            raise ValueError("Insufficient funds in the source account")

        # Debit and credit.
        source["balance"] -= total_amount
        target["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:,.2f} from {source_acct} to "
        f"{target_acct} completed successfully by user '{employee_id}'."
    )