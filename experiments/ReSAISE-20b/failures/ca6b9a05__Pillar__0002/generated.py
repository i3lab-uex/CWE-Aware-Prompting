from decimal import Decimal, InvalidOperation
import threading

# Example accounts database. In a real system this would be replaced by a secure data store.
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user1", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user2", "balance": Decimal("500.00")},
    # ... more accounts
}

# Global lock to guard concurrent access to the accounts database.
_ACCOUNTS_LOCK = threading.Lock()


def _get_account(account_number: str) -> dict:
    """Retrieve an account from the database in a thread‑safe manner."""
    with _ACCOUNTS_LOCK:
        acct = ACCOUNTS_DB.get(account_number)
        if not acct:
            raise ValueError(f"Account {account_number} does not exist.")
        return acct


def move_funds(u_id: str, u_role: str,
               source_account: str, destination_account: str,
               money: float) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    u_id : str
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    money : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are invalid, insufficient funds, or negative amounts.
    """
    # Validate money amount
    try:
        transfer_amount = Decimal(str(money))
    except InvalidOperation:
        raise ValueError("Invalid monetary value.")

    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src_acct = _get_account(source_account)
    dst_acct = _get_account(destination_account)

    # Authorization logic
    authorized = False

    if u_role == "bank_admin":
        authorized = True
    elif u_role == "account_owner" and src_acct["owner_id"] == u_id:
        authorized = True
    # customer_service role is not allowed to transfer funds directly

    if not authorized:
        raise PermissionError("User does not have permission to move funds.")

    # Perform transfer atomically
    with _ACCOUNTS_LOCK:
        if src_acct["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        src_acct["balance"] -= transfer_amount
        dst_acct["balance"] += transfer_amount

    return (f"Successfully transferred {transfer_amount:.2f} from "
            f"{source_account} to {destination_account}.")