import urllib.parse as urlparse
from typing import List

# Domains that are considered safe for redirection outside the main application.
PERMITTED_DOMAINS: List[str] = ["trusted.com", "another-safe.org"]


def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    target_param : str
        The user supplied URL path or full URL.

    Returns
    -------
    str
        A fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the target URL is not within the application domain or an allowed external domain.
    """
    # Parse the base application URL
    main_parts = urlparse.urlparse(main_url)
    if not main_parts.scheme or not main_parts.netloc:
        raise ValueError("Invalid main_url")

    # Parse the target parameter
    target_parts = urlparse.urlparse(target_param)

    # If target is a relative path, simply join it to the base URL
    if not target_parts.scheme and not target_parts.netloc:
        # Ensure it starts with a slash
        path = target_parts.path or "/"
        if not path.startswith("/"):
            path = "/" + path
        # Preserve any query string or fragment from the original target_param
        full_path = urlparse.urlunparse(("", "", path, target_parts.params,
                                         target_parts.query, target_parts.fragment))
        return urlparse.urljoin(main_url, full_path)

    # If target is an absolute URL, verify its domain
    if target_parts.scheme not in {"http", "https"}:
        raise ValueError("Target URL scheme must be http or https")

    # Compare netlocs: allow if same as main_url or in PERMITTED_DOMAINS
    target_netloc = target_parts.netloc.lower()
    main_netloc = main_parts.netloc.lower()

    if target_netloc == main_netloc:
        # Same domain: safe to redirect
        return target_param

    if any(target_netloc.endswith("." + d) or target_netloc == d for d in PERMITTED_DOMAINS):
        # Allowed external domain
        return target_param

    raise ValueError("Untrusted redirect URL: {}".format(target_param))