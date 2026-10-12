from decimal import Decimal, InvalidOperation
from typing import Dict

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": Decimal("1500.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": Decimal("500.00")},
    # Add more accounts as needed.
}

def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transaction.
    initiator_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
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
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        For invalid transfer amounts or insufficient funds.
    """
    # Validate accounts exist
    try:
        src = ACCOUNTS_DB[withdraw_account]
        dst = ACCOUNTS_DB[deposit_account]
    except KeyError as e:
        raise KeyError(f"Account {e.args[0]} does not exist.") from None

    # Authorization: owner of source account or privileged role
    authorized = (
        initiator_role in {"bank_admin", "customer_service"} or
        (initiator_role == "account_owner" and initiator_id == src["owner_id"])
    )
    if not authorized:
        raise PermissionError("Unauthorized access: insufficient privileges to transfer funds.")

    # Validate transfer amount
    try:
        amount = Decimal(str(transfer_value))
    except InvalidOperation:
        raise ValueError("Transfer value must be a numeric type.") from None

    if amount <= 0:
        raise ValueError("Transfer value must be greater than zero.")

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient balance in the source account.")

    # Perform transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account '{withdraw_account}' "
        f"to account '{deposit_account}' completed successfully."
    )

# Example usage:
if __name__ == "__main__":
    try:
        msg = shift_funds(
            initiator_id="user1",
            initiator_role="account_owner",
            withdraw_account="ACC123",
            deposit_account="ACC456",
            transfer_value=200.00
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")