import datetime

# Example accounts database.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 2500.00},
    # Add more accounts as needed
}

def _log_transaction(sender: str, receiver: str, amount: float) -> None:
    """Simple logger for transactions (could be extended to write to a file or audit system)."""
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] Transfer of ${amount:.2f} from {sender} to {receiver}")

def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    account_holder : str
        User ID initiating the transaction.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transaction.
    KeyError
        If either account number does not exist in ACCOUNTS_DB.
    ValueError
        If the fund_amount is non‑positive or insufficient balance.
    """
    # Basic validation of inputs
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    try:
        withdraw_acc = ACCOUNTS_DB[withdrawal_account]
        recv_acc = ACCOUNTS_DB[receiving_account]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}") from None

    # Authorization logic
    authorized = False
    if user_role == "bank_admin" or user_role == "customer_service":
        authorized = True
    elif user_role == "account_owner" and withdraw_acc["owner_id"] == account_holder:
        authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transaction.")

    # Check sufficient funds
    if withdraw_acc["balance"] < fund_amount:
        raise ValueError("Insufficient balance in withdrawal account.")

    # Perform the transfer atomically (simple lockless operation)
    withdraw_acc["balance"] -= fund_amount
    recv_acc["balance"] += fund_amount

    # Log the transaction (placeholder for a real audit trail)
    _log_transaction(withdrawal_account, receiving_account, fund_amount)

    return (
        f"Transfer of ${fund_amount:.2f} from {withdrawal_account} to "
        f"{receiving_account} completed successfully."
    )

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = send_funds(
#             account_holder="user123",
#             user_role="account_owner",
#             withdrawal_account="ACC1001",
#             receiving_account="ACC2002",
#             fund_amount=300.00
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")