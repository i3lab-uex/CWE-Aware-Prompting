from __future__ import annotations

import typing as _t

# Example account database. In a real system this would be persisted securely.
ACCOUNTS_DB: dict[str, dict[str, _t.Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.00},
    # Add more accounts as needed
}

# Roles that are allowed to perform transfers
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}


def _get_account(acc_number: str) -> dict[str, _t.Any]:
    """Retrieve an account from the database or raise KeyError."""
    try:
        return ACCOUNTS_DB[acc_number]
    except KeyError as exc:
        raise ValueError(f"Account {acc_number!r} does not exist.") from exc


def _is_authorized(
    identifier: str,
    role: str,
    source_acc: dict[str, _t.Any],
    destination_acc: dict[str, _t.Any],
) -> bool:
    """
    Determine if the requester is allowed to perform a transfer.
    - account_owner: can only move money from accounts they own.
    - bank_admin: unrestricted.
    - customer_service: cannot move funds between arbitrary accounts,
      but can transfer to/from an account they own if the source or destination
      matches their ownership.
    """
    if role not in ALLOWED_ROLES:
        return False

    # Bank admins have full rights
    if role == "bank_admin":
        return True

    # Account owners can transfer from accounts they own
    if role == "account_owner" and source_acc["owner_id"] == identifier:
        return True

    # Customer service can transfer if at least one side is owned by them
    if role == "customer_service":
        return (
            source_acc["owner_id"] == identifier
            or destination_acc["owner_id"] == identifier
        )

    return False


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float,
) -> str:
    """
    Transfer money between accounts with proper authorization checks.

    Parameters
    ----------
    identifier : str
        The unique ID of the individual requesting the transfer.
    role : str
        Role of the requester ('account_owner', 'bank_admin', 'customer_service').
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the requester is not authorized to perform this transfer.
    ValueError
        If accounts do not exist, the amount is invalid,
        or insufficient funds.
    """
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = _get_account(source_acc)
    dst = _get_account(destination_acc)

    if not _is_authorized(identifier, role, src, dst):
        raise PermissionError(
            f"User {identifier!r} with role {role!r} is not authorized to transfer "
            f"from {source_acc!r} to {destination_acc!r}"
        )

    if src["balance"] < value:
        raise ValueError(
            f"Insufficient funds in source account {source_acc!r}. "
            f"Available: {src['balance']:.2f}, required: {value:.2f}"
        )

    # Perform the transfer
    src["balance"] -= value
    dst["balance"] += value

    return (
        f"Transfer of {value:.2f} from {source_acc!r} to "
        f"{destination_acc!r} completed successfully."
    )