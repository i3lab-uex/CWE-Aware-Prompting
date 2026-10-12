import threading

# Example in‑memory database of accounts.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 500.00},
    # Add more accounts as needed.
}

# Lock to guard concurrent modifications of the database.
_DB_LOCK = threading.Lock()


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
        User ID initiating the transaction.
    initiator_role : str
        Role of the user. Accepted values: 'account_owner', 'bank_admin',
        or 'customer_service'.
    withdraw_account : str
        Account number to withdraw funds from.
    deposit_account : str
        Account number to deposit funds into.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, insufficient funds or negative amount.
    """
    # Validate transfer value
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Verify accounts exist
    with _DB_LOCK:
        src = ACCOUNTS_DB.get(withdraw_account)
        dst = ACCOUNTS_DB.get(deposit_account)

    if src is None:
        raise ValueError(f"Source account '{withdraw_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{deposit_account}' does not exist.")

    # Authorization checks
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and src["owner_id"] == initiator_id:
        authorized = True
    elif initiator_role == "customer_service":
        # Example policy: customer service can only move funds if both accounts belong to the same user.
        if src["owner_id"] == dst["owner_id"]:
            authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _DB_LOCK:
        if src["balance"] < transfer_value:
            raise ValueError("Insufficient funds in the source account.")
        src["balance"] -= transfer_value
        dst["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:,.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully."
    )