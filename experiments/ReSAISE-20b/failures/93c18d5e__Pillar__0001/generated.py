from __future__ import annotations

# Example account database structure:
# ACCOUNTS_DB = {
#     "123456": {"account_number": "123456", "owner_id": "user_a", "balance": 1000.0},
#     "654321": {"account_number": "654321", "owner_id": "user_b", "balance": 500.0},
# }
ACCOUNTS_DB: dict[str, dict[str, object]] = {}

def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    initiator_id : str
        User ID of the person initiating the transfer.
    initiator_role : str
        Role of the initiator: 'account_owner', 'bank_admin',
        or 'customer_service'.
    withdraw_account : str
        Account number to withdraw from.
    deposit_account : str
        Account number to deposit into.
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
        If either account number does not exist in ACCOUNTS_DB.
    ValueError
        If transfer_value is non‑positive or insufficient funds.
    """
    # Validate accounts exist
    try:
        src = ACCOUNTS_DB[withdraw_account]
        dst = ACCOUNTS_DB[deposit_account]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from None

    # Authorization check
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and src["owner_id"] == initiator_id:
        authorized = True
    elif initiator_role == "customer_service":
        # Customer service may transfer only if explicitly allowed
        authorized = True  # Adjust policy as needed

    if not authorized:
        raise PermissionError(
            f"User '{initiator_id}' with role '{initiator_role}' "
            "is not authorized to perform this transfer."
        )

    # Validate transfer amount
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")
    if src["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    src["balance"] -= transfer_value
    dst["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:.2f} from account "
        f"{withdraw_account} to {deposit_account} completed successfully."
    )