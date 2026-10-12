import re
from urllib.parse import urlparse, urljoin

# List of external domains that are explicitly allowed for redirection
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

# Regular expression to validate that a URL scheme is either http or https
_SCHEME_RE = re.compile(r"^(https?):$")


def _is_allowed_domain(netloc: str, base_netloc: str) -> bool:
    """
    Determine whether the provided netloc is either the same as the base
    application domain or is in the list of APPROVED_DOMAINS.
    """
    # Normalise netloc by stripping any port
    host = netloc.split(":")[0].lower()
    base_host = base_netloc.split(":")[0].lower()

    if host == base_host:
        return True

    # Check against approved domains (case‑insensitive)
    return host in {d.lower() for d in APPROVED_DOMAINS}


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL based on the user‑provided `redirect_param`.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The full redirect URL that is guaranteed to be within the application
        domain or an approved external domain.

    Raises
    ------
    ValueError
        If the resulting URL points outside of allowed domains or uses an
        unsafe scheme.
    """
    # Parse the base application URL to get its components
    parsed_app = urlparse(app_url)
    if not _SCHEME_RE.match(parsed_app.scheme):
        raise ValueError(f"Invalid application URL scheme: {parsed_app.scheme}")

    # Parse the redirect parameter
    parsed_redirect = urlparse(redirect_param)

    if not parsed_redirect.scheme:
        # Relative path: join with the application base URL
        final_url = urljoin(app_url, redirect_param)
    else:
        # Absolute URL: ensure it uses http or https
        if not _SCHEME_RE.match(parsed_redirect.scheme):
            raise ValueError(f"Unsupported scheme in redirect: {parsed_redirect.scheme}")

        # Ensure the domain is allowed
        if not _is_allowed_domain(parsed_redirect.netloc, parsed_app.netloc):
            raise ValueError(
                f"Redirect domain '{parsed_redirect.netloc}' is not approved."
            )
        final_url = redirect_param

    # Final safety check: parse the resulting URL and confirm scheme
    parsed_final = urlparse(final_url)
    if not _SCHEME_RE.match(parsed_final.scheme):
        raise ValueError(f"Final URL has invalid scheme: {parsed_final.scheme}")

    # Return the fully resolved, safe redirect URL
    return final_url