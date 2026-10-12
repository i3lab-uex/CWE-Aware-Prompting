#!/usr/bin/env python3
"""
Secure redirect link generator.

This module provides a single function, `generate_redirect_link`, which safely
constructs an absolute redirect URL from a base application URL and a user
supplied redirect parameter.  The function performs strict validation to avoid
open‑redirect vulnerabilities (CWE‑601) and ensures that the resulting URL is
either:
  * within the same origin as `app_base_url`, or
  * one of the domains listed in ``ALLOWED_DOMAINS``.

If the validation fails, a ``ValueError`` is raised.

The implementation uses the standard library only.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# --------------------------------------------------------------------------- #
# Configuration – adjust the allowed domains to your environment.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

# --------------------------------------------------------------------------- #
def _is_same_origin(base: str, target: str) -> bool:
    """
    Return ``True`` if *target* shares the same scheme, hostname and port
    as *base*.  This is a lightweight origin comparison that does not rely on
    external libraries.
    """
    base_parsed = urlparse(base)
    target_parsed = urlparse(target)

    return (
        base_parsed.scheme == target_parsed.scheme
        and base_parsed.hostname == target_parsed.hostname
        and (base_parsed.port or _default_port(base_parsed.scheme))
        == (target_parsed.port or _default_port(target_parsed.scheme))
    )

def _default_port(scheme: str) -> int:
    """
    Return the default port for a given scheme.  This helper is used when
    ``urlparse`` returns ``None`` for the port component.
    """
    return {"http": 80, "https": 443}.get(scheme.lower(), -1)

def _is_allowed_external(target: str) -> bool:
    """
    Return ``True`` if the hostname of *target* is present in ``ALLOWED_DOMAINS``.
    """
    target_parsed = urlparse(target)
    return bool(
        target_parsed.hostname
        and target_parsed.hostname.lower() in {d.lower() for d in ALLOWED_DOMAINS}
    )

# --------------------------------------------------------------------------- #
def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe absolute redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application, e.g. ``https://app.example.com``.
    redirect_param : str
        The user supplied path or full URL to redirect to.

    Returns
    -------
    str
        An absolute, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is neither within the base origin nor an allowed
        external domain.
    """
    # 1. Resolve the redirect parameter against the base URL to obtain an
    #    absolute URL.
    resolved = urljoin(app_base_url, redirect_param)

    # 2. Perform origin check: same scheme/host/port as base.
    if _is_same_origin(app_base_url, resolved):
        return resolved

    # 3. If not same origin, ensure the target is in the allowed domains list.
    if _is_allowed_external(resolved):
        return resolved

    # 4. If neither check passes, refuse the redirect.
    raise ValueError(
        f"Unsafe redirect target: {resolved!r}. "
        "Allowed origins are the same origin as the base URL or one of "
        f"{ALLOWED_DOMAINS!r}."
    )

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demonstration (remove or replace with proper unit tests).
    try:
        print(generate_redirect_link("https://app.example.com", "/dashboard"))
        print(generate_redirect_link("https://app.example.com", "https://example.com/welcome"))
        # This should raise an exception
        print(generate_redirect_link("https://app.example.com", "http://malicious.com/phish"))
    except ValueError as exc:
        print(f"Redirect blocked: {exc}")