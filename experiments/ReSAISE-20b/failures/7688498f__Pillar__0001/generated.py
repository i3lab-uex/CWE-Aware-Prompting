import threading

# Simulated accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "USR001", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "USR002", "balance": 500.0},
    # Add more accounts as needed
}

# Lock for thread‑safe updates
_db_lock = threading.Lock()


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts if the user is authorized.

    Parameters
    ----------
    u_identifier : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    account_from : str
        Account number to debit.
    account_to : str
        Account number to credit.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid accounts, insufficient funds, or negative amount.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    with _db_lock:
        src = ACCOUNTS_DB.get(account_from)
        dst = ACCOUNTS_DB.get(account_to)

    if not src or not dst:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if u_role == "bank_admin":
        # Admins can transfer between any accounts
        authorized = True

    elif u_role == "account_owner":
        # Owner can transfer only from accounts they own
        if src["owner_id"] == u_identifier:
            authorized = True

    # Other roles (e.g., customer_service) are not allowed to transfer funds
    if not authorized:
        raise PermissionError(
            f"User '{u_identifier}' with role '{u_role}' is not authorized "
            "to perform this transfer."
        )

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account.")

        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from '{account_from}' to "
        f"'{account_to}' completed successfully."
    )