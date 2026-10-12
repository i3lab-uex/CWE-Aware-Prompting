import urllib.parse

# Domains that are explicitly allowed for redirection even if they differ from the base domain
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL by combining `base_url` with the user-provided
    `next_param`. The function ensures that the resulting URL points to either:
        * The same host as `base_url`, or
        * One of the hosts listed in ALLOWED_DOMAINS.

    Parameters:
        base_url (str): The application's base URL.
        next_param (str): The raw 'next' parameter supplied by the user.

    Returns:
        str: A fully qualified URL safe for redirection.

    Raises:
        ValueError: If the final URL resolves to an unsafe domain.
    """
    # Parse base and next URLs
    parsed_base = urllib.parse.urlparse(base_url)
    parsed_next = urllib.parse.urlparse(next_param)

    # If next_param is an absolute URL, ensure its domain is allowed
    if parsed_next.scheme and parsed_next.netloc:
        # Resolve the host, accounting for possible IPv6 brackets
        host = parsed_next.hostname or ""
        if not (host == parsed_base.hostname or host in ALLOWED_DOMAINS):
            raise ValueError(f"Disallowed redirect domain: {host}")

        # Return the next_param as is (already absolute)
        return parsed_next.geturl()

    # For relative URLs, join with the base URL
    joined = urllib.parse.urljoin(base_url, next_param)

    # Parse the resulting URL to confirm safety
    parsed_joined = urllib.parse.urlparse(joined)
    host = parsed_joined.hostname or ""

    if not (host == parsed_base.hostname or host in ALLOWED_DOMAINS):
        raise ValueError(f"Disallowed redirect domain after joining: {host}")

    return joined