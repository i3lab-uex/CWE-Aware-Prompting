import urllib.parse

# External domains that are explicitly allowed for redirects.
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    next_path : str
        The user-provided path or URL to redirect to.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain.
    """
    # Resolve the target URL relative to the primary URL.
    candidate = urllib.parse.urljoin(primary_url, next_path)

    # Parse both URLs to inspect their components.
    primary_parsed = urllib.parse.urlparse(primary_url)
    candidate_parsed = urllib.parse.urlparse(candidate)

    # Helper to normalize netloc (handle default ports).
    def _normalize_netloc(parsed):
        host = parsed.hostname or ""
        port = parsed.port
        # Exclude default ports for http/https.
        if (parsed.scheme == "http" and port in (None, 80)) or \
           (parsed.scheme == "https" and port in (None, 443)):
            return host.lower()
        return f"{host}:{port}".lower()

    primary_netloc = _normalize_netloc(primary_parsed)
    candidate_netloc = _normalize_netloc(candidate_parsed)

    # Check if the candidate is within the same domain or an allowed external domain.
    if candidate_netloc != primary_netloc and candidate_netloc not in SAFE_DOMAINS:
        raise ValueError(f"Redirect to untrusted domain: {candidate_netloc}")

    # Ensure the candidate uses a safe scheme (http or https).
    if candidate_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {candidate_parsed.scheme}")

    return candidate