from decimal import Decimal, getcontext
from typing import Dict

# Set precision high enough for typical financial calculations
getcontext().prec = 28


# Example accounts database structure
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": Decimal("1500.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": Decimal("2000.00")},
    # Add more accounts as needed
}


def _get_account(account_number: str) -> Dict:
    """Retrieve account dict from ACCOUNTS_DB, raising KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account '{account_number}' does not exist.") from exc


def _authorize(u_id: str, u_role: str, source_account: Dict) -> None:
    """
    Verify that the user is authorized to initiate a transfer from the source account.
    Raises PermissionError if unauthorized.
    """
    if u_role == "bank_admin":
        # Bank admins can transfer from any account
        return

    if u_role == "account_owner":
        # Owner must own the source account
        if source_account["owner_id"] != u_id:
            raise PermissionError("Account owner can only transfer from their own accounts.")
        return

    # Other roles (e.g., customer_service) are not allowed to initiate transfers
    raise PermissionError(f"User role '{u_role}' is not authorized to transfer funds.")


def move_funds(u_id: str, u_role: str, source_account: str,
               destination_account: str, money: float) -> str:
    """
    Transfer `money` from `source_account` to `destination_account`.

    Parameters
    ----------
    u_id : str
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    money : float
        Amount to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the transfer amount is invalid or insufficient funds.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    src_acc = _get_account(source_account)
    dst_acc = _get_account(destination_account)

    # Authorization check
    _authorize(u_id, u_role, src_acc)

    transfer_amount = Decimal(str(money))

    # Ensure sufficient funds
    if src_acc["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform the transfer atomically
    src_acc["balance"] -= transfer_amount
    dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from '{source_account}' "
        f"to '{destination_account}' completed successfully."
    )