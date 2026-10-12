from typing import Dict

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 500.0},
    # ... add more accounts as needed
}

def _is_authorized(
    initiator_id: str,
    initiator_role: str,
    account_number: str
) -> bool:
    """
    Determines whether the initiator is allowed to act on the specified account.
    - 'account_owner' can act only on their own account.
    - 'bank_admin' and 'customer_service' have full privileges.
    """
    if initiator_role in {"bank_admin", "customer_service"}:
        return True

    # For account_owner, ensure the account belongs to them.
    account = ACCOUNTS_DB.get(account_number)
    if not account:
        return False  # Non‑existent account → not authorized
    return initiator_role == "account_owner" and account["owner_id"] == initiator_id


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Moves money from withdraw_account to deposit_account.

    Raises PermissionError if the initiator lacks proper authorization.
    Returns a confirmation string on success.
    """
    # Validate input types and values
    if not isinstance(transfer_value, (int, float)) or transfer_value <= 0:
        raise ValueError("Transfer value must be a positive number.")

    # Authorization checks
    if not _is_authorized(initiator_id, initiator_role, withdraw_account):
        raise PermissionError(
            f"User {initiator_id} does not have permission to withdraw from account {withdraw_account}"
        )
    if not _is_authorized(initiator_id, initiator_role, deposit_account):
        raise PermissionError(
            f"User {initiator_id} does not have permission to deposit into account {deposit_account}"
        )

    # Fetch accounts
    withdraw_acc = ACCOUNTS_DB.get(withdraw_account)
    deposit_acc = ACCOUNTS_DB.get(deposit_account)

    if withdraw_acc is None or deposit_acc is None:
        raise KeyError("One or both accounts do not exist in the database.")

    # Ensure sufficient funds
    if withdraw_acc["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform the transfer atomically (simplified for demo purposes)
    withdraw_acc["balance"] -= transfer_value
    deposit_acc["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:.2f} from account {withdraw_account} "
        f"to account {deposit_account} completed successfully."
    )