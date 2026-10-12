import threading

# Example in‑memory database of accounts
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 500.0},
    # Add more accounts as needed
}

# A global lock to protect concurrent modifications of the accounts database.
_ACCOUNTS_LOCK = threading.RLock()


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator. Accepted values are:
            * 'account_owner'
            * 'bank_admin'
            * 'customer_service'
    withdraw_account : str
        Account number from which funds will be withdrawn.
    deposit_account : str
        Target account number where the funds will be transferred.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer completes.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform this transfer.
    KeyError
        If either account number does not exist in the database.
    ValueError
        If the transfer value is non‑positive or insufficient funds are available.
    """

    # Basic validation
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")

    # Retrieve account data safely
    with _ACCOUNTS_LOCK:
        if withdraw_account not in ACCOUNTS_DB:
            raise KeyError(f"Withdraw account '{withdraw_account}' does not exist.")
        if deposit_account not in ACCOUNTS_DB:
            raise KeyError(f"Deposit account '{deposit_account}' does not exist.")

        withdraw_acc = ACCOUNTS_DB[withdraw_account]
        deposit_acc = ACCOUNTS_DB[deposit_account]

        # Authorization checks
        if position == "bank_admin":
            authorized = True
        elif position == "account_owner":
            # Owner can only transfer from their own account
            authorized = withdraw_acc["owner_id"] == initiator_id
        elif position == "customer_service":
            # Customer service can only transfer between accounts that belong to the same owner
            authorized = (
                withdraw_acc["owner_id"] == deposit_acc["owner_id"]
                and withdraw_acc["owner_id"] == initiator_id
            )
        else:
            authorized = False

        if not authorized:
            raise PermissionError(
                f"User '{initiator_id}' with role '{position}' is not authorized "
                f"to transfer from account '{withdraw_account}'."
            )

        # Check sufficient funds
        if withdraw_acc["balance"] < transfer_value:
            raise ValueError(
                f"Insufficient funds in account '{withdraw_account}'. "
                f"Available: {withdraw_acc['balance']:.2f}, required: {transfer_value:.2f}."
            )

        # Perform the transfer atomically
        withdraw_acc["balance"] -= transfer_value
        deposit_acc["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from account '{withdraw_account}' "
        f"to account '{deposit_account}' completed successfully."
    )