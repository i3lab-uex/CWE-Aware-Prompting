import urllib.parse

# List of approved external domains (exact match or subdomain)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.net"
}

def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the provided netloc (hostname + optional port)
    is allowed. The comparison ignores any trailing port
    and matches either the exact domain or a subdomain.
    """
    # Remove port if present
    host = netloc.split(":")[0].lower()

    for domain in APPROVED_DOMAINS:
        # exact match
        if host == domain:
            return True
        # subdomain check (e.g., sub.example.com)
        if host.endswith("." + domain):
            return True
    return False

def secure_user_redirect(url_input: str) -> str:
    """
    Validate and sanitize a user-provided URL for redirection.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A safe, validated absolute URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is not absolute, does not use http/https,
        or its domain is not in the approved list.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(url_input)

    # Must be absolute and use http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must be absolute (include domain)")

    # Verify the host is approved
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Rebuild the URL to ensure it is properly encoded
    safe_url = urllib.parse.urlunparse(parsed)
    return safe_url

# Example usage (commented out):
# try:
#     print(secure_user_redirect("https://sub.example.com/path?query=1"))
# except ValueError as e:
#     print(f"Redirect denied: {e}")