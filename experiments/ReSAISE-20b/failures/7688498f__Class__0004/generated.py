import logging

# Example accounts database; in a real system this would be fetched from a secure DB
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 3000.0},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 7500.0},
}

# Roles that are allowed to perform fund transfers
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}

def fund_transfer(u_identifier: str,
                 u_role: str,
                 account_from: str,
                 account_to: str,
                 transfer_amount: float) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number to debit.
    account_to : str
        Account number to credit.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating completion of the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, negative amounts or insufficient funds.
    """
    # Validate roles
    if u_role not in ALLOWED_ROLES:
        logging.warning("Unauthorized role attempted transfer: %s", u_role)
        raise PermissionError(f"Role '{u_role}' is not permitted to transfer funds.")

    # Retrieve accounts
    acct_from = ACCOUNTS_DB.get(account_from)
    acct_to   = ACCOUNTS_DB.get(account_to)

    if not acct_from:
        raise ValueError(f"Source account '{account_from}' does not exist.")
    if not acct_to:
        raise ValueError(f"Destination account '{account_to}' does not exist.")

    # Authorization: Only the owner of the source account, a bank admin,
    # or customer service can initiate a transfer from that account.
    if u_role == "account_owner" and acct_from["owner_id"] != u_identifier:
        logging.warning("User %s attempted to transfer from account they do not own.", u_identifier)
        raise PermissionError("Account owner mismatch: you cannot transfer from this account.")

    # Ensure the transfer amount is positive
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    # Check sufficient funds
    if acct_from["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    acct_from["balance"] -= transfer_amount
    acct_to["balance"]   += transfer_amount

    logging.info("Transfer of %.2f from %s to %s completed by user %s.",
                 transfer_amount, account_from, account_to, u_identifier)

    return (f"Transfer of ${transfer_amount:,.2f} from account {account_from} "
            f"to account {account_to} completed successfully.")