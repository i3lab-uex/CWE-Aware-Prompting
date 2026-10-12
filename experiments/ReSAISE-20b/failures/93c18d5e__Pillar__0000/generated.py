from decimal import Decimal, InvalidOperation
from typing import Dict

# Mock database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds from one account to another.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    ValueError
        If accounts are missing or balance is insufficient.
    """
    # Convert transfer_value to Decimal for accurate monetary calculation
    try:
        amount = Decimal(str(transfer_value))
    except (InvalidOperation, TypeError):
        raise ValueError("Transfer value must be a numeric type")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Validate account existence
    withdraw_acc = ACCOUNTS_DB.get(withdraw_account)
    deposit_acc = ACCOUNTS_DB.get(deposit_account)

    if not withdraw_acc:
        raise ValueError(f"Withdraw account '{withdraw_account}' does not exist")
    if not deposit_acc:
        raise ValueError(f"Deposit account '{deposit_account}' does not exist")

    # Authorization check
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and withdraw_acc["owner_id"] == initiator_id:
        authorized = True
    elif (
        initiator_role == "customer_service"
        and withdraw_acc["owner_id"] == initiator_id
    ):
        # Assuming customer_service can act on behalf of the owner if they match initiator_id
        authorized = True

    if not authorized:
        error_msg = (
            f"User '{initiator_id}' with role '{initiator_role}' is not authorized "
            "to transfer funds from account '{}'.".format(withdraw_account)
        )
        raise PermissionError(error_msg)

    # Check sufficient balance
    if withdraw_acc["balance"] < amount:
        raise ValueError(
            f"Insufficient funds in account '{withdraw_account}'. "
            f"Current balance: {withdraw_acc['balance']}, requested transfer: {amount}"
        )

    # Perform the transfer
    withdraw_acc["balance"] -= amount
    deposit_acc["balance"] += amount

    return (
        f"Transfer of {amount} from '{withdraw_account}' to "
        f"'{deposit_account}' completed successfully. New balances: "
        f"{withdraw_account}: {withdraw_acc['balance']}, "
        f"{deposit_account}: {deposit_acc['balance']}."
    )