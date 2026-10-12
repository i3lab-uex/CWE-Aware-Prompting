import logging
from typing import Dict

# Example accounts database (in a real system this would be replaced by a persistent store)
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}

# Configure logging for audit trail
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(message)s]",
)

def _is_authorized(
    person_id: str,
    role: str,
    source_account: Dict,
) -> bool:
    """
    Determine whether the person is allowed to initiate a transfer from the source account.
    - The owner of the account can always move money from it.
    - Bank admins and customer service agents have blanket permission.
    """
    if role in {"bank_admin", "customer_service"}:
        return True
    return source_account["owner_id"] == person_id


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from one account to another after performing authorization checks.
    Raises PermissionError if the user is not authorized.

    Parameters
    ----------
    person_id : str
        Identifier of the user initiating the transaction.
    role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    source_account : str
        Account number to withdraw from.
    destination_account : str
        Account number to deposit into.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.
    """
    # Validate inputs
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive")

    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise KeyError(f"Source account {source_account} does not exist")
    if dst is None:
        raise KeyError(f"Destination account {destination_account} does not exist")

    # Authorization check
    if not _is_authorized(person_id, role, src):
        logging.warning(
            "Unauthorized transfer attempt by %s (role=%s) from %s to %s",
            person_id,
            role,
            source_account,
            destination_account,
        )
        raise PermissionError("User is not authorized to move money from the source account")

    # Balance check
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account")

    # Perform the transfer atomically (simulated here with simple updates)
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    # Log the transaction for audit purposes
    logging.info(
        "User %s (role=%s) transferred %.2f from %s to %s",
        person_id,
        role,
        transfer_amount,
        source_account,
        destination_account,
    )

    return (
        f"Transfer of {transfer_amount:.2f} from account {source_account} "
        f"to account {destination_account} completed successfully."
    )