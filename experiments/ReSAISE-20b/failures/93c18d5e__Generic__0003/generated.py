from decimal import Decimal, InvalidOperation
import threading

# Sample accounts database. In a real system this would be persisted in a DB.
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": Decimal("1500.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": Decimal("500.00")},
    # add more accounts as needed
}

# Lock to simulate atomic updates in a multi‑threaded environment.
_db_lock = threading.Lock()


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    initiator_id : str
        User ID that is requesting the transfer.
    initiator_role : str
        Role of the user. Allowed values: 'account_owner', 'bank_admin',
        or 'customer_service'.
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer was performed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, negative amounts or insufficient funds.
    """
    # Validate transfer value
    try:
        amount = Decimal(str(transfer_value))
    except InvalidOperation:
        raise ValueError("Transfer value must be a numeric type")

    if amount <= 0:
        raise ValueError("Transfer value must be positive")

    # Check accounts exist
    with _db_lock:
        if withdraw_account not in ACCOUNTS_DB:
            raise ValueError(f"Withdraw account '{withdraw_account}' does not exist")
        if deposit_account not in ACCOUNTS_DB:
            raise ValueError(f"Deposit account '{deposit_account}' does not exist")

        withdraw_acct = ACCOUNTS_DB[withdraw_account]
        deposit_acct = ACCOUNTS_DB[deposit_account]

    # Authorization checks
    authorized = False

    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "customer_service":
        # customer service can transfer only if they have explicit permission,
        # here we assume it's allowed for demonstration.
        authorized = True
    elif initiator_role == "account_owner":
        # Owner can only transfer from their own account
        if initiator_id == withdraw_acct["owner_id"]:
            authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer")

    # Perform the transfer atomically
    with _db_lock:
        if withdraw_acct["balance"] < amount:
            raise ValueError("Insufficient funds in the withdrawal account")

        withdraw_acct["balance"] -= amount
        deposit_acct["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account '{withdraw_account}' "
        f"to account '{deposit_account}' completed successfully."
    )