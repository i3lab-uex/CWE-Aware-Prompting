import urllib.parse

# Domains that are allowed for external redirects.
SAFE_DOMAINS = [
    "example.com",
    "trusted.example.org",
    # Add more trusted domains here.
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL based on the user-provided `next_path`.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_path : str
        The path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not within the
        application or in `SAFE_DOMAINS`.
    """
    # Parse primary URL once.
    base = urllib.parse.urlparse(primary_url)

    if not base.scheme or not base.netloc:
        raise ValueError("primary_url must be a valid absolute URL")

    # Parse the next_path.
    parsed_next = urllib.parse.urlparse(next_path)

    if parsed_next.scheme:
        # `next_path` is an absolute URL. Validate its domain.
        next_netloc = parsed_next.netloc.lower()
        primary_netloc = base.netloc.lower()

        if next_netloc != primary_netloc and next_netloc not in SAFE_DOMAINS:
            raise ValueError(
                f"Redirect target '{next_path}' is not allowed: "
                f"domain {next_netloc} is outside the trusted list."
            )
        # It's safe; return as-is.
        return next_path

    # Relative path: join with the base URL's scheme and netloc.
    # urllib.parse.urljoin handles leading slashes correctly.
    full_url = urllib.parse.urljoin(f"{base.scheme}://{base.netloc}", next_path)

    # After joining, ensure we didn't escape the base domain via a trick
    # like '../../../evil.com'.
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() != base.netloc.lower():
        raise ValueError(
            f"Redirect target '{next_path}' resolves to a different domain: "
            f"{final_parsed.netloc}"
        )

    return full_url