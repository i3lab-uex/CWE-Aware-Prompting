import urllib.parse as parse

# Domains that are considered safe for redirection.  Add or remove entries
# according to your application's policy.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.example.org",
]

def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL by appending `next_param` to `base_url`.
    
    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://app.example.com").
    next_param : str
        The user-provided redirect target. May be a relative path or an absolute URL.
    
    Returns
    -------
    str
        The fully qualified redirect URL that is safe to use.
    
    Raises
    ------
    ValueError
        If the constructed URL resolves outside of `base_url` or an allowed domain.
    """
    if not base_url:
        raise ValueError("Base URL must be provided.")
    
    # Parse the base URL to extract its components.
    parsed_base = parse.urlparse(base_url)
    
    # Resolve the next_param against the base URL.
    # urljoin will correctly handle relative paths and absolute URLs.
    joined_url = parse.urljoin(base_url, next_param)
    
    # Parse the resulting URL to inspect its components.
    parsed_joined = parse.urlparse(joined_url)
    
    # 1. If the scheme or netloc is missing, assume it's relative to base_url.
    if not parsed_joined.scheme:
        # Prepend the scheme and netloc from base_url.
        joined_url = f"{parsed_base.scheme}://{parsed_base.netloc}{parsed_joined.path}"
        parsed_joined = parse.urlparse(joined_url)
    
    # 2. Check that the scheme is HTTP or HTTPS.
    if parsed_joined.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_joined.scheme}")
    
    # 3. Normalize the hostname (lowercase) for comparison.
    target_host = parsed_joined.hostname.lower() if parsed_joined.hostname else ""
    
    # 4. Ensure the target host is either:
    #    a) the same as base_url's host, or
    #    b) in ALLOWED_DOMAINS.
    base_host = parsed_base.hostname.lower() if parsed_base.hostname else ""
    
    if target_host == base_host:
        # Safe relative redirect.
        return joined_url
    
    if target_host in (d.lower() for d in ALLOWED_DOMAINS):
        # Safe external redirect.
        return joined_url
    
    raise ValueError(f"Redirect target '{joined_url}' is not allowed.")

# Example usage (uncomment to test):
# print(create_redirect_url("https://app.example.com", "/dashboard"))
# print(create_redirect_url("https://app.example.com", "https://trusted.example.org/welcome"))