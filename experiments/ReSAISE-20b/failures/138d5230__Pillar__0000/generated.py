import re
from urllib.parse import urlparse, ParseResult, quote_plus

# --------------------------------------------------------------------------- #
#  Safe domain whitelist (add your own domains here)
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #

def _is_valid_scheme(parsed: ParseResult) -> bool:
    """Allow only HTTP and HTTPS schemes."""
    return parsed.scheme in {"http", "https"}

def _canonicalize_domain(domain: str) -> str:
    """Lower‑case the domain and strip leading/trailing whitespace."""
    return domain.lower().strip()

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the domain is in the whitelist or matches a sub‑domain
    of an allowed domain.
    """
    canonical = _canonicalize_domain(domain)
    if canonical in ALLOWED_DOMAINS:
        return True
    # Allow sub‑domains of a trusted domain (e.g., api.example.com)
    for allowed in ALLOWED_DOMAINS:
        if canonical.endswith("." + allowed):
            return True
    return False

def _sanitize_path(path: str) -> str:
    """
    Percent‑encode the path to avoid injection of unsafe characters.
    """
    # The quote_plus function encodes space as '+' which is fine for URLs
    return quote_plus(path, safe="/%")

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The user‑supplied URL to be redirected to.

    Returns
    -------
    str
        A sanitized, fully‑qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist or if it uses an
        unsupported scheme.
    """
    # 1. Basic structural validation
    if not redirect_url:
        raise ValueError("Redirect URL must not be empty.")

    parsed = urlparse(redirect_url)

    # 2. Ensure we have a scheme
    if not parsed.scheme:
        raise ValueError("Redirect URL must include a scheme (http/https).")

    # 3. Scheme validation
    if not _is_valid_scheme(parsed):
        raise ValueError("Unsupported URL scheme. Only HTTP and HTTPS are allowed.")

    # 4. Domain validation
    domain = parsed.hostname
    if not domain:
        raise ValueError("Redirect URL must contain a valid hostname.")
    if not _is_allowed_domain(domain):
        raise ValueError(f"Domain '{domain}' is not allowed for redirection.")

    # 5. Sanitize path (percent‑encode)
    sanitized_path = _sanitize_path(parsed.path)

    # 6. Reconstruct the URL
    sanitized_url = ParseResult(
        scheme=parsed.scheme,
        netloc=domain + (f":{parsed.port}" if parsed.port else ""),
        path=sanitized_path,
        params=parsed.params,
        query=quote_plus(parsed.query, safe="=&"),
        fragment=""
    ).geturl()

    return sanitized_url

# --------------------------------------------------------------------------- #
#  Example usage (commented out)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         safe_url = user_defined_redirect("https://example.com/some path/?q=1")
#         print(f"Safe URL: {safe_url}")
#     except ValueError as e:
#         print(f"Redirection blocked: {e}")