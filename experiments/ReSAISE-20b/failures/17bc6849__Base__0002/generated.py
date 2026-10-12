import re
from urllib.parse import urlparse, urljoin

# Example list of external domains considered safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add other domains as needed
]

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if a domain is either the same as the app's base domain
    or listed in ALLOWED_DOMAINS.
    """
    # Strip port if present
    domain = domain.split(":")[0]
    return domain in ALLOWED_DOMAINS

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (e.g. 'https://app.example.com/')
    forward_param : str
        The user‑supplied redirect target.  Can be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain or is malformed.
    """
    # Normalise and parse the base URL
    parsed_base = urlparse(app_home_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_home_url must be a valid absolute URL")

    # Determine if forward_param is an absolute URL
    parsed_forward = urlparse(forward_param)

    if parsed_forward.scheme in ("http", "https"):
        # Absolute URL supplied by the user
        if not parsed_forward.netloc:
            raise ValueError("forward_param must contain a network location")

        # Validate the domain
        if not _is_allowed_domain(parsed_forward.netloc):
            raise ValueError(f"Domain '{parsed_forward.netloc}' is not allowed for redirects")

        # Ensure the URL uses a secure scheme
        if parsed_forward.scheme != "https":
            raise ValueError("Only HTTPS URLs are allowed for external redirects")

        # Return the absolute URL as is
        return forward_param

    else:
        # Treat as a relative path; guard against traversal attacks
        if re.search(r"(?<!:)//", forward_param):
            # Disallow double slashes that could lead to absolute URLs
            raise ValueError("Relative path contains disallowed '//' sequence")

        # Join with the base URL
        redirect_url = urljoin(app_home_url, forward_param)

        # Final sanity check: the netloc must match the base domain
        parsed_redirect = urlparse(redirect_url)
        if parsed_redirect.netloc != parsed_base.netloc:
            raise ValueError("Redirect points outside the application domain")

        return redirect_url