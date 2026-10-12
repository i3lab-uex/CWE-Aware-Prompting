# Banking fund transfer implementation

from typing import Dict, Any

# Example in‑memory accounts database
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}

def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Move funds from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    initiator_role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message or error message if unauthorized.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If the transfer_value is invalid or insufficient funds.
    """
    # Basic validation
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts
    try:
        withdraw_acc = ACCOUNTS_DB[withdraw_account]
        deposit_acc = ACCOUNTS_DB[deposit_account]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from None

    # Authorization check
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and withdraw_acc["owner_id"] == initiator_id:
        authorized = True
    elif initiator_role == "customer_service":
        # For example, customer service can only transfer if explicitly allowed
        authorized = False  # Adjust policy as required

    if not authorized:
        raise PermissionError("Unauthorized access for fund transfer")

    # Sufficient funds check
    if withdraw_acc["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdrawal account")

    # Perform the transfer atomically
    withdraw_acc["balance"] -= transfer_value
    deposit_acc["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully."
    )