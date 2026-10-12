import urllib.parse

# A whitelist of fully-qualified domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.net",
}

def _is_approved_domain(domain: str) -> bool:
    """
    Check if the supplied domain is in the approved list.
    The check is case‑insensitive and strips any trailing port number.
    """
    # Remove possible userinfo, path, query or fragment
    parsed = urllib.parse.urlparse(domain)
    host = parsed.hostname or ""
    return host.lower() in APPROVED_DOMAINS


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL against a whitelist of approved domains and
    return the normalized absolute URL that can be safely used for redirection.

    Parameters
    ----------
    url_input : str
        The URL string supplied by the user.

    Returns
    -------
    str
        A fully-qualified, validated URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https scheme,
        or its domain is not in the approved list.
    """
    # Parse and validate basic structure
    parsed = urllib.parse.urlparse(url_input)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Ensure domain is approved
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain {parsed.hostname!r} is not approved")

    # Reconstruct the URL to avoid any hidden characters or fragments
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            "",  # discard fragment
        )
    )

    return safe_url