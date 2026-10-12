import urllib.parse

# External domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.example.org",
    # Add other domains as needed
]


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a secure redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (must contain scheme and netloc).
    forward_param : str
        The user‑supplied redirect target.  It can be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the target is not within the base domain, or if an external domain
        is not in :data:`ALLOWED_DOMAINS`, or if the target contains an unsafe
        scheme (e.g. ``javascript:``).
    """
    # ---------- Validate base URL ----------
    parsed_base = urllib.parse.urlparse(app_home_url)
    if not (parsed_base.scheme and parsed_base.netloc):
        raise ValueError(f"Invalid base URL: {app_home_url!r}")

    # ---------- Parse the forward parameter ----------
    parsed_forward = urllib.parse.urlparse(forward_param)

    # Reject schemes that could lead to XSS or other attacks
    if parsed_forward.scheme.lower() in {"javascript", "data", "vbscript"}:
        raise ValueError(f"Unsafe scheme detected in forward parameter: {forward_param!r}")

    # ---------- Handle absolute URLs ----------
    if parsed_forward.scheme in {"http", "https"}:
        # Absolute URL – check that the domain is allowed
        if parsed_forward.netloc.lower() not in (d.lower() for d in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect domain not allowed: {parsed_forward.netloc!r}")

        # Use the absolute URL as is (no further validation needed)
        redirect_url = forward_param
    else:
        # ---------- Handle relative URLs ----------
        if parsed_forward.netloc:
            # A netloc in a supposedly relative URL is suspicious
            raise ValueError(f"Relative redirect contains a netloc: {forward_param!r}")

        # Resolve the relative path against the base URL
        redirect_url = urllib.parse.urljoin(app_home_url, forward_param)

        # Ensure the resolved URL stays within the base domain
        parsed_redirect = urllib.parse.urlparse(redirect_url)
        if parsed_redirect.netloc.lower() != parsed_base.netloc.lower():
            raise ValueError(
                f"Redirect URL {redirect_url!r} does not belong to the base domain {parsed_base.netloc!r}"
            )

    return redirect_url