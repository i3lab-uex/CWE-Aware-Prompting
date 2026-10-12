from decimal import Decimal, getcontext, InvalidOperation
from typing import Dict

# Set precision high enough for financial calculations
getcontext().prec = 28


# Sample accounts database; in a real system this would be fetched from persistent storage
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": Decimal("500.00")},
    # ... additional accounts
}


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts after validating authorization and balance.

    Parameters
    ----------
    u_identifier : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role of the individual (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number to debit.
    account_to : str
        Account number to credit.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transaction was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, amount invalid, or insufficient funds.
    """

    # Basic validation of inputs
    if account_from == account_to:
        raise ValueError("Source and destination accounts must differ.")
    try:
        amount = Decimal(str(transfer_amount))
    except (InvalidOperation, TypeError):
        raise ValueError("Transfer amount must be a numeric value.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src_account = ACCOUNTS_DB.get(account_from)
    dst_account = ACCOUNTS_DB.get(account_to)

    if src_account is None or dst_account is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if u_role == "bank_admin":
        authorized = True  # Admin can transfer between any accounts
    elif u_role == "account_owner" and src_account["owner_id"] == u_identifier:
        authorized = True  # Owner can transfer from their own account
    elif u_role == "customer_service":
        # Customer service may need additional checks; here we allow if both accounts belong to the same owner
        authorized = src_account["owner_id"] == dst_account["owner_id"]

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Check sufficient balance
    if src_account["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically (simplified for this example)
    src_account["balance"] -= amount
    dst_account["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {account_from} to {account_to} "
        f"completed successfully."
    )


# Example usage (uncomment for testing)
# try:
#     msg = fund_transfer("user1", "account_owner", "ACC123", "ACC456", 200.0)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")