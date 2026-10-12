import urllib.parse
from typing import List

# Example list of external domains considered safe for redirection.
ALLOWED_DOMAINS: List[str] = [
    "https://example.com",
    "https://trustedpartner.org",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_redirect_param : str
        The URL path or address the user wants to navigate to after login.
        Can be a relative path ("/dashboard") or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves outside of the base domain and is not in
        ALLOWED_DOMAINS.
    """
    # Normalise the base URL (ensure it has a scheme and trailing slash)
    parsed_base = urllib.parse.urlparse(domain_base_url)
    if not parsed_base.scheme:
        raise ValueError("Base URL must include a scheme (http or https).")
    base_netloc = parsed_base.netloc.lower()

    # Resolve the next redirect parameter against the base URL
    joined_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Parse the resolved URL to inspect its components
    parsed_joined = urllib.parse.urlparse(joined_url)
    joined_netloc = parsed_joined.netloc.lower()

    # Helper to check if a URL is in the allowed domains list
    def _is_allowed(url: str) -> bool:
        for allowed in ALLOWED_DOMAINS:
            parsed_allowed = urllib.parse.urlparse(allowed)
            if (
                parsed_allowed.scheme.lower() == parsed_joined.scheme.lower()
                and parsed_allowed.netloc.lower() == joined_netloc
            ):
                return True
        return False

    # Determine if the redirect is safe:
    # 1. It's relative to the base domain (same netloc)
    # 2. Or it's an absolute URL whose domain is in ALLOWED_DOMAINS
    if joined_netloc != base_netloc and not _is_allowed(joined_url):
        raise ValueError(
            f"Redirect URL '{joined_url}' is not within the allowed domains."
        )

    # Return the fully qualified, safe URL
    return joined_url


# ----------------- Example usage (uncomment to test) -----------------
# if __name__ == "__main__":
#     base = "https://app.example.com"
#     for param in ["/profile", "/dashboard?next=/home",
#                   "https://trustedpartner.org/login", 
#                   "http://malicious.com/phish"]:
#         try:
#             print(construct_redirect_link(base, param))
#         except ValueError as e:
#             print(f"Invalid redirect: {e}")