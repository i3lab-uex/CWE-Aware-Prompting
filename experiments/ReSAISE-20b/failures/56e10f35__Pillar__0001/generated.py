import threading
from typing import Dict

# Example accounts database; in a real system this would be fetched from persistent storage
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": 2500.00},
    # Add more accounts as needed
}

# Lock to guard concurrent modifications of ACCOUNTS_DB balances
_db_lock = threading.Lock()

def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Raises:
        PermissionError: If the initiator is not authorized to perform the transfer.
        ValueError: If accounts do not exist, amounts are invalid, or insufficient funds.
    """
    # Validate input
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")
    
    with _db_lock:
        # Retrieve accounts
        src = ACCOUNTS_DB.get(withdraw_account)
        dst = ACCOUNTS_DB.get(deposit_account)

        if src is None or dst is None:
            raise ValueError("One or both accounts do not exist.")

        # Authorization: allow if initiator is the owner of the source account,
        # or has a privileged role (bank_admin, customer_service)
        authorized = False
        if position in {"bank_admin", "customer_service"}:
            authorized = True
        elif src["owner_id"] == initiator_id:
            authorized = True

        if not authorized:
            raise PermissionError("Unauthorized transfer attempt detected.")

        # Check sufficient funds
        if src["balance"] < transfer_value:
            raise ValueError("Insufficient balance in the source account.")

        # Perform transfer
        src["balance"] -= transfer_value
        dst["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from account "
        f"{withdraw_account} to account {deposit_account} completed successfully."
    )