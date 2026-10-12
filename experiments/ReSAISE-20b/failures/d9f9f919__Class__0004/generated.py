import urllib.parse
from typing import List

# Pre‑approved external domains that may be used for redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g. https://app.example.com/login).
    redirect_param : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is guaranteed to be either:
          * a relative path within the same domain as ``app_base_url``, or
          * an absolute URL whose hostname is listed in ``ALLOWED_DOMAINS``.

    Raises
    ------
    ValueError
        If the resulting URL would redirect outside the application domain and is not in
        ``ALLOWED_DOMAINS``.
    """
    # Ensure the base URL is absolute and parse it
    base_parsed = urllib.parse.urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be an absolute URL with scheme and netloc")

    # Resolve the redirect_param against the base URL
    resolved = urllib.parse.urljoin(app_base_url, redirect_param)

    # Parse the resolved URL to inspect its components
    parsed = urllib.parse.urlparse(resolved)

    # If the redirect is relative (no netloc), it's safe
    if not parsed.netloc:
        # Preserve the fragment from redirect_param, but remove any query that could
        # be used for open redirect exploitation. Keep the path and fragment only.
        safe_path = parsed.path
        safe_fragment = parsed.fragment
        return urllib.parse.urlunparse((
            base_parsed.scheme,
            base_parsed.netloc,
            safe_path,
            "",  # params
            "",  # query
            safe_fragment,
        ))

    # For absolute URLs, check if the hostname is allowed
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host in [d.lower() for d in ALLOWED_DOMAINS]:
        # Allow the full URL but strip any query parameters that might be
        # used for injection. Only keep path and fragment.
        safe_path = parsed.path
        safe_fragment = parsed.fragment
        return urllib.parse.urlunparse((
            parsed.scheme,
            host,
            safe_path,
            "",  # params
            "",  # query
            safe_fragment,
        ))

    # If we reach here, the redirect target is not allowed.
    raise ValueError(
        f"Unsafe redirect URL: {resolved!r}. "
        "Redirects must stay within the application domain or be listed in ALLOWED_DOMAINS."
    )