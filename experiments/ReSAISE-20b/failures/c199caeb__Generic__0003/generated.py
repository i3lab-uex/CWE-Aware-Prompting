import re
from urllib.parse import urlparse, urljoin

# List of external domains that are considered safe for redirection.
APPROVED_DOMAINS = [
    "example.com",
    "trusted-site.org",
]

def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL based on the user-provided `redirect_param`.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g. "https://myapp.com").
    redirect_param : str
        User-provided path or full URL to redirect to after login.

    Returns
    -------
    str
        The final, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an approved external domain.
    """
    if not redirect_param:
        # Default to the base app URL if no redirect is specified.
        return app_url

    parsed_app = urlparse(app_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError(f"Invalid base application URL: {app_url!r}")

    # Resolve the redirect target relative to the app URL.
    candidate = urljoin(app_url, redirect_param)

    parsed_candidate = urlparse(candidate)

    # If the candidate is a relative path (no scheme/netloc), it's safe.
    if not parsed_candidate.scheme and not parsed_candidate.netloc:
        return candidate

    # For absolute URLs, ensure the domain is either the same as the app or in approved list.
    candidate_domain = parsed_candidate.hostname
    if not candidate_domain:
        raise ValueError(f"Redirect URL does not contain a valid hostname: {candidate!r}")

    # Normalize domains to lowercase for comparison.
    candidate_domain = candidate_domain.lower()
    app_domain = parsed_app.hostname.lower()

    # Allow same domain or any approved external domains.
    if candidate_domain != app_domain and candidate_domain not in {d.lower() for d in APPROVED_DOMAINS}:
        raise ValueError(f"Redirect URL {candidate!r} is not allowed (domain: {candidate_domain})")

    # Reconstruct the URL to ensure it contains a scheme and netloc.
    safe_url = parsed_candidate.geturl()
    return safe_url