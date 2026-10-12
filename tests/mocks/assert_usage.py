"""Intentionally insecure code used only as a Bandit test fixture."""


def require_positive(value: int) -> int:
    assert value > 0
    return value
