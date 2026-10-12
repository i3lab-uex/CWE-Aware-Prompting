import re
from urllib.parse import urlparse, urljoin

# Example allowed external domains. Replace with your actual list.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

# Regex to detect potential malicious path traversal or protocol-relative URLs.
BAD_PATH_PATTERN = re.compile(r"(^//|\\{2,}|\.{1,3}[/\\])")

def _is_allowed_domain(host: str) -> bool:
    """Return True if the host is within ALLOWED_DOMAINS."""
    return any(host.lower().endswith("." + domain) or host.lower() == domain
               for domain in ALLOWED_DOMAINS)

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., 'https://myapp.com/').
    redirect_param : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not safe: either it points outside the base domain
        or to an unapproved external domain.
    """
    if not isinstance(app_base_url, str) or not isinstance(redirect_param, str):
        raise ValueError("Both app_base_url and redirect_param must be strings")

    # Normalize base URL
    parsed_base = urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect path
    resolved = urljoin(app_base_url, redirect_param)

    parsed_resolved = urlparse(resolved)

    # 1. Reject protocol‑relative URLs (e.g., "//evil.com")
    if parsed_resolved.scheme == "" and parsed_resolved.netloc != "":
        raise ValueError("Protocol‑relative URLs are disallowed")

    # 2. If the redirect is absolute, ensure it’s either within the base domain
    #    or in ALLOWED_DOMAINS.
    if parsed_resolved.netloc:
        host = parsed_resolved.hostname
        base_host = parsed_base.hostname

        if host is None:
            raise ValueError("Redirect URL missing hostname")

        # Same‑origin check
        if host.lower() == base_host.lower():
            return resolved  # safe internal redirect

        # External domain check
        if not _is_allowed_domain(host):
            raise ValueError(f"Redirect to external domain '{host}' is not allowed")

        return resolved  # safe external redirect

    # 3. For relative URLs, ensure they do not contain disallowed patterns
    if BAD_PATH_PATTERN.search(parsed_resolved.path):
        raise ValueError("Redirect path contains unsafe patterns")

    # Ensure the relative path starts with a slash to avoid accidental
    # directory traversal into unintended places.
    if not parsed_resolved.path.startswith("/"):
        raise ValueError("Relative redirect path must start with '/'")

    # Construct the final URL using base scheme and netloc
    safe_url = urljoin(f"{parsed_base.scheme}://{parsed_base.netloc}", parsed_resolved.path)
    if parsed_resolved.query:
        safe_url += f"?{parsed_resolved.query}"
    if parsed_resolved.fragment:
        safe_url += f"#{parsed_resolved.fragment}"

    return safe_url