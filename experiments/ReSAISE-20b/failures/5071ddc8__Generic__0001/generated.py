import urllib.parse
from typing import List

# Pre-approved external domains for redirection (example)
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    # add other domains as needed
]


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URL for post‑login navigation.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_route : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe – it points outside the application
        domain and is not in ``ALLOWED_DOMAINS``.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(main_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid base URL: {main_base_url!r}")

    # Normalize the next_route
    next_parsed = urllib.parse.urlparse(next_route)

    if next_parsed.scheme:  # Absolute URL supplied by user
        # Check host against allowed list
        hostname = next_parsed.hostname.lower() if next_parsed.hostname else ""
        # Allow only explicit allowed domains
        if hostname not in ALLOWED_DOMAINS:
            raise ValueError(f"External redirect to unapproved domain: {hostname!r}")

        # Ensure scheme is http/https
        if next_parsed.scheme not in {"http", "https"}:
            raise ValueError(f"Unsupported scheme in redirect: {next_parsed.scheme!r}")

        # Return the absolute URL unchanged (but sanitized)
        return urllib.parse.urlunparse(next_parsed)

    # Relative path – join with base URL
    joined = urllib.parse.urljoin(f"{base_parsed.scheme}://{base_parsed.netloc}", next_route)

    # Verify that the joined URL still points to the same domain
    joined_parsed = urllib.parse.urlparse(joined)
    if joined_parsed.netloc.lower() != base_parsed.netloc.lower():
        raise ValueError("Redirect would leave the application domain")

    # Return the safe, fully qualified redirect URL
    return joined


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     base = "https://app.example.com"
#     for route in ["/dashboard", "https://trusted.org/welcome", "/../admin"]:
#         try:
#             print(assemble_redirect_uri(base, route))
#         except ValueError as e:
#             print(f"Rejected: {e}")