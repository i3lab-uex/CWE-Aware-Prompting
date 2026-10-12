import urllib.parse
from typing import List

# Pre‑approved external domains for redirection (example)
ALLOWED_DOMAINS: List[str] = [
    "https://trusted.example.com",
    "https://another-allowed-site.org",
]

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL for post‑login navigation.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        User supplied redirect target; may be a relative path or an absolute URL.

    Returns
    -------
    str
        Fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside the application domain and is not
        in the ALLOWED_DOMAINS list.
    """
    # Ensure base URL has a scheme
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        raise ValueError(f"Base URL must include a scheme: {app_base_url}")

    # Resolve redirect target
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    parsed_resolved = urllib.parse.urlparse(resolved)
    # If the resolved URL is relative, urljoin will keep it relative to base
    if not parsed_resolved.scheme:
        # Relative path: safe by definition
        return resolved

    # For absolute URLs, check domain safety
    base_netloc = parsed_base.netloc.lower()
    target_netloc = parsed_resolved.netloc.lower()

    # 1. Same domain check (case‑insensitive)
    if target_netloc == base_netloc:
        return resolved

    # 2. Allowed external domains check
    for allowed in ALLOWED_DOMAINS:
        parsed_allowed = urllib.parse.urlparse(allowed)
        if target_netloc == parsed_allowed.netloc.lower():
            # Ensure scheme matches allowed domain (default to https if missing)
            if parsed_allowed.scheme and parsed_allowed.scheme != parsed_resolved.scheme:
                continue
            return resolved

    # If we reach here, the URL is unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")

# Example usage:
if __name__ == "__main__":
    base = "https://app.example.com"
    # relative path
    print(build_redirect_link(base, "/dashboard"))
    # same domain absolute URL
    print(build_redirect_link(base, "https://app.example.com/profile"))
    # allowed external domain
    print(build_redirect_link(base, "https://trusted.example.com/home"))
    # unsafe external domain (will raise ValueError)
    try:
        print(build_redirect_link(base, "https://malicious.com/phishing"))
    except ValueError as e:
        print(e)