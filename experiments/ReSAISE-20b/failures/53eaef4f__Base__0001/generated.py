from urllib.parse import urlparse, urljoin

# Domains that are considered safe for external redirects.
SAFE_DOMAINS = [
    "example.com",
    "trusted.org",
    # Add other trusted domains here.
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    next_path : str
        The user-specified path or full URL to redirect to after login.

    Returns
    -------
    str
        A fully qualified, safe URL to redirect the user.

    Raises
    ------
    ValueError
        If `next_path` resolves to a URL that is not within the application domain
        or one of the explicitly allowed external domains.
    """
    # Normalise the primary URL (ensure it ends with a slash for urljoin).
    base = primary_url.rstrip("/") + "/"

    # Parse the user supplied path.
    parsed_next = urlparse(next_path)

    # If next_path is an absolute URL (has scheme), validate it.
    if parsed_next.scheme in ("http", "https"):
        # Resolve the full URL to compare with primary_url.
        target_url = next_path
    else:
        # It's a relative path; safely combine with base.
        target_url = urljoin(base, next_path)

    # Parse the resolved URL to inspect its components.
    parsed_target = urlparse(target_url)

    # Resolve primary domain for comparison.
    parsed_base = urlparse(base)

    # Function to compare netlocs, ignoring default ports.
    def clean_netloc(netloc: str) -> str:
        host, _, port = netloc.partition(":")
        # Remove default ports for http/https.
        if (parsed_target.scheme == "http" and port in ("80", "")) or \
           (parsed_target.scheme == "https" and port in ("443", "")):
            return host.lower()
        return f"{host.lower()}:{port}"

    target_netloc = clean_netloc(parsed_target.netloc)
    base_netloc = clean_netloc(parsed_base.netloc)

    # Check if the target is within the same application domain.
    if target_netloc == base_netloc:
        return target_url

    # Otherwise, check against the list of safe external domains.
    if any(target_netloc.endswith("." + d.lower()) or target_netloc == d.lower()
           for d in SAFE_DOMAINS):
        return target_url

    # If we reach here, the URL is not trusted.
    raise ValueError(f"Untrusted redirect target: {target_url}")