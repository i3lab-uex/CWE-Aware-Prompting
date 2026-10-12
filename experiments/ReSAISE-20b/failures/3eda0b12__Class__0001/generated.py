import re
from urllib.parse import urlparse, urljoin

# Domains that are allowed for external redirects.
PERMITTED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com/").
    target_param : str
        The URL path or full URL supplied by the user.

    Returns
    -------
    str
        A fully qualified redirect URL that is either relative to `main_url`
        or points to one of the permitted external domains.

    Raises
    ------
    ValueError
        If the resulting URL points outside of the application domain and is
        not in `PERMITTED_DOMAINS`.
    """
    # Normalize the main URL (ensure it has a scheme and trailing slash)
    base = urlparse(main_url)
    if not base.scheme or not base.netloc:
        raise ValueError("`main_url` must be a valid absolute URL.")
    if not main_url.endswith("/"):
        main_url = f"{main_url}/"

    # Parse the target parameter
    parsed_target = urlparse(target_param)

    # If the target is a relative path, just join it with the base URL
    if not parsed_target.scheme and not parsed_target.netloc:
        return urljoin(main_url, target_param)

    # If the target is absolute, validate its domain
    if parsed_target.scheme in ("http", "https"):
        # Check against the application's own domain
        if parsed_target.netloc == base.netloc:
            return target_param

        # Check against permitted external domains
        hostname = parsed_target.hostname or ""
        if any(re.fullmatch(rf"{re.escape(domain)}", hostname) for domain in PERMITTED_DOMAINS):
            return target_param

    # Anything else is disallowed
    raise ValueError("Redirect URL is not permitted.")