import urllib.parse

# Domains that are considered safe for external redirection.
ALLOWED_DOMAINS = ["example.com", "trusted.org"]


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL by validating the user-provided `next_param`.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://myapp.com/").
    next_param : str
        The user-supplied redirect target. It may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to be safe.

    Raises
    ------
    ValueError
        If the target URL resolves to a domain that is neither the same as
        `base_url` nor in :data:`ALLOWED_DOMAINS`.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(base_url)

    # Resolve the target relative to the base URL
    resolved = urllib.parse.urljoin(base_url, next_param)

    # Parse the resolved URL to inspect its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the resolved URL has no network location (netloc), it is relative
    if not target_parsed.netloc:
        # Ensure the path starts with a slash to avoid relative traversal
        safe_path = urllib.parse.urljoin("/", target_parsed.path)
        return base_parsed.scheme + "://" + base_parsed.netloc + safe_path

    # If it is an absolute URL, verify that the domain is allowed
    target_domain = target_parsed.hostname

    # Compare against base domain (allow subdomains of the base)
    if target_domain and target_domain.endswith(base_parsed.hostname):
        return resolved

    # Allow only explicitly whitelisted domains
    if target_domain and any(target_domain == d or target_domain.endswith("." + d) for d in ALLOWED_DOMAINS):
        return resolved

    # If none of the checks passed, raise an error
    raise ValueError(f"Redirect target '{next_param}' is not allowed.")


# Example usage
if __name__ == "__main__":
    try:
        print(create_redirect_url("https://myapp.com/", "/dashboard"))
        print(create_redirect_url("https://myapp.com/", "https://trusted.org/page"))
        # This will raise ValueError
        print(create_redirect_url("https://myapp.com/", "https://evil.com/"))
    except ValueError as exc:
        print("Redirect blocked:", exc)