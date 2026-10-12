import threading

# Example accounts database (global)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 2000.0},
    # Add more accounts as needed
}

# A lock to protect concurrent modifications of the accounts database
_ACCOUNTS_LOCK = threading.Lock()


def execute_transfer(identifier: str, role: str,
                     source_acc: str, destination_acc: str,
                     value: float) -> str:
    """
    Transfer funds between two accounts.

    Parameters
    ----------
    identifier : str
        Identifier of the individual requesting the transfer.
    role : str
        Role of the requester ('account_owner', 'bank_admin',
        'customer_service', etc.).
    source_acc : str
        Account number from which funds will be withdrawn.
    destination_acc : str
        Account number to which funds will be deposited.
    value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer was completed.

    Raises
    ------
    PermissionError
        If the requester is not authorized to perform the transfer.
    KeyError
        If either account does not exist in `ACCOUNTS_DB`.
    ValueError
        If the transfer value is invalid (negative or insufficient funds).
    """
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts; raise KeyError if missing
    try:
        src = ACCOUNTS_DB[source_acc]
        dst = ACCOUNTS_DB[destination_acc]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}") from None

    # Authorization checks
    if role == "bank_admin":
        authorized = True
    elif role == "account_owner" and src["owner_id"] == identifier:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt.")

    # Perform the transfer atomically
    with _ACCOUNTS_LOCK:
        if src["balance"] < value:
            raise ValueError("Insufficient funds in source account.")
        src["balance"] -= value
        dst["balance"] += value

    return (
        f"Transfer of {value:.2f} from {source_acc} to "
        f"{destination_acc} completed successfully."
    )