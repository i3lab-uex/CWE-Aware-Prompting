import threading

# Example accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed
}

# Global lock to protect concurrent access to the accounts database
_ACCOUNTS_LOCK = threading.Lock()


def _is_authorized(identifier: str, role: str,
                   source_acc: dict, dest_acc: dict) -> bool:
    """
    Determine whether the requesting user is allowed to perform a transfer.
    - 'account_owner': must own both source and destination accounts.
    - 'bank_admin': has full access.
    - any other role: denied.
    """
    if role == "bank_admin":
        return True
    if role == "account_owner":
        return (source_acc["owner_id"] == identifier and
                dest_acc["owner_id"] == identifier)
    # Other roles are not permitted to transfer funds
    return False


def execute_transfer(identifier: str, role: str,
                     source_acc: str, destination_acc: str,
                     value: float) -> str:
    """
    Transfer `value` from `source_acc` to `destination_acc`.

    Parameters
    ----------
    identifier : str
        Identifier of the individual requesting the transfer.
    role : str
        Role held by the individual (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acc : str
        Account number to withdraw funds from.
    destination_acc : str
        Account number to deposit funds into.
    value : float
        Monetary amount to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, value invalid, or insufficient funds.
    """
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _ACCOUNTS_LOCK:
        src = ACCOUNTS_DB.get(source_acc)
        dst = ACCOUNTS_DB.get(destination_acc)

        if src is None or dst is None:
            raise ValueError("One or both accounts do not exist.")

        if not _is_authorized(identifier, role, src, dst):
            raise PermissionError("Unauthorized transfer attempt.")

        if src["balance"] < value:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer atomically
        src["balance"] -= value
        dst["balance"] += value

    return (f"Transfer of {value:.2f} from {source_acc} to "
            f"{destination_acc} completed successfully.")