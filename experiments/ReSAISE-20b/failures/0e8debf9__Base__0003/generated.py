import urllib.parse

# Pre‑approved external domains that may be used in redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    # Add more domains as needed
]


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    post_login_param : str
        The URL path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(auth_base_url)

    # Resolve the user‑supplied target relative to the base
    resolved = urllib.parse.urljoin(auth_base_url, post_login_param)

    # Parse the resolved URL to examine its components
    target_parsed = urllib.parse.urlparse(resolved)

    # If the target is a relative URL, it will have an empty netloc.
    # In that case we consider it safe because it's within the base domain.
    if not target_parsed.netloc:
        return resolved

    # Normalise the netloc (lowercase) for comparison
    target_netloc = target_parsed.netloc.lower()

    # Check if the netloc is exactly the same as the base's
    if target_netloc == base_parsed.netloc.lower():
        return resolved

    # Otherwise, ensure the target domain is in the whitelist
    if not any(target_netloc.endswith("." + d) or target_netloc == d for d in ALLOWED_DOMAINS):
        raise ValueError(f"Unsafe redirect target: {resolved}")

    # If we reach here, the domain is trusted; return the resolved URL
    return resolved


# Example usage (for testing purposes only)
if __name__ == "__main__":
    base = "https://app.example.com/"
    # Safe relative path
    print(generate_redirect_uri(base, "/dashboard"))

    # Safe absolute URL to a whitelisted domain
    print(generate_redirect_uri(base, "https://trusted.org/home"))

    # Unsafe absolute URL (will raise ValueError)
    try:
        print(generate_redirect_uri(base, "https://evil.com/phish"))
    except ValueError as e:
        print(e)