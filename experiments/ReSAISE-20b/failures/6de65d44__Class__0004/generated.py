# move_money.py

"""
Move money between accounts with proper authorization checks.
"""

from typing import Dict
import threading

# Sample in-memory database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 3000.00},
    # Add more accounts as needed
}

# Lock for thread‑safe balance updates
_db_lock = threading.Lock()


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Transfer money from source_account to destination_account.

    Args:
        person_id (str): ID of the user initiating the transfer.
        role (str): Role of the user ('account_owner', 'bank_admin',
                    or 'customer_service').
        source_account (str): Account number to withdraw from.
        destination_account (str): Account number to deposit into.
        transfer_amount (float): Amount of money to transfer.

    Returns:
        str: Success message if the transfer completes.

    Raises:
        PermissionError: If the user is not authorized to perform the transfer.
        ValueError: If accounts are missing, amount invalid, or insufficient funds.
    """

    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if not src or not dst:
        raise ValueError("One or both accounts do not exist.")

    # Authorization check
    authorized = False

    if role == "bank_admin":
        authorized = True  # Admin can transfer between any accounts
    elif role == "account_owner" and src["owner_id"] == person_id:
        authorized = True
    # customer_service has no transfer rights

    if not authorized:
        raise PermissionError("Unauthorized access to transfer funds.")

    # Ensure source has enough balance
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    with _db_lock:
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = move_money(
#             person_id="user123",
#             role="account_owner",
#             source_account="ACC1001",
#             destination_account="ACC2002",
#             transfer_amount=1500.00
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")