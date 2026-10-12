from typing import Dict

# Sample accounts database for demonstration purposes.
ACCOUNTS_DB: Dict[str, Dict[str, any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 750.00},
    # Add more accounts as needed.
}

def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float
) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Parameters
    ----------
    identifier : str
        The unique ID of the individual requesting the transfer.
    role : str
        Role of the requester (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acc : str
        Account number from which funds will be debited.
    destination_acc : str
        Account number to which funds will be credited.
    value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the requester is not authorized to perform the transfer.
    ValueError
        If accounts are missing, balance insufficient or amount invalid.
    """
    # Basic input validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve account records
    src = ACCOUNTS_DB.get(source_acc)
    dst = ACCOUNTS_DB.get(destination_acc)

    if src is None or dst is None:
        raise ValueError("Source or destination account does not exist.")

    # Authorization: allow if requester is bank admin, customer service,
    # or the owner of the source account.
    authorized = (
        role in {"bank_admin", "customer_service"} or
        (role == "account_owner" and identifier == src["owner_id"])
    )

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt detected.")

    # Sufficient funds check
    if src["balance"] < value:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer
    src["balance"] -= value
    dst["balance"] += value

    return (
        f"Transfer of {value:.2f} from {source_acc} to "
        f"{destination_acc} completed successfully."
    )