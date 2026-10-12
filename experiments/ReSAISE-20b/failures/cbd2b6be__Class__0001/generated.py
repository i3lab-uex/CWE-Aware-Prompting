import urllib.parse
from typing import Iterable

# A whitelist of domains that are allowed to be used as callback hosts.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = [
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
]


def _is_allowed_domain(domain: str) -> bool:
    """
    Check whether a domain is in the ALLOWED_CALLBACK_DOMAINS list.
    The check is case‑insensitive and ignores leading/trailing whitespace.
    """
    domain = domain.strip().lower()
    return domain in (d.lower() for d in ALLOWED_CALLBACK_DOMAINS)


def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a full OAuth callback URL and ensure its domain is trusted.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path segment for the callback (e.g., "/oauth/callback").
    token_state : str
        A unique string used as a state parameter.

    Returns
    -------
    str
        The fully qualified callback URL with the state query param appended.

    Raises
    ------
    ValueError
        If the resolved URL does not belong to an allowed domain.
    """
    # Normalize the base URL (ensure it ends with a slash for urljoin to work correctly)
    if not main_url.endswith("/"):
        base = f"{main_url}/"
    else:
        base = main_url

    # Ensure the redirect path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = f"/{redirect_path}"

    # Build the full URL
    callback_url = urllib.parse.urljoin(base, redirect_path)

    # Append the state query parameter
    parsed = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = token_state
    new_query = urllib.parse.urlencode(query_params)

    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate the domain
    netloc = urllib.parse.urlparse(final_url).netloc
    # Extract hostname (strip port if present)
    host = netloc.split(":")[0]
    if not _is_allowed_domain(host):
        raise ValueError(f"Disallowed callback domain: {host}")

    return final_url