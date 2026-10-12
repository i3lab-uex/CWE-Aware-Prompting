import urllib.parse
from typing import Set

# Domains that are explicitly allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_callback : str
        The relative or absolute path to the callback handler (e.g. "/oauth/callback").
    session_id : str
        A unique identifier used as the OAuth state parameter.

    Returns
    -------
    str
        The fully qualified callback URL including a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL points to a domain that is not in
        `ALLOWED_CALLBACK_DOMAINS` and does not match the host domain.
    """
    # Normalise the base URL (ensure it has a scheme)
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme:
        raise ValueError("host_url must include a scheme (http:// or https://)")

    # Resolve the callback path against the host URL
    full_url = urllib.parse.urljoin(host_url, path_callback)

    parsed_full = urllib.parse.urlparse(full_url)
    callback_domain = parsed_full.hostname

    # Validate domain
    if callback_domain is None:
        raise ValueError("callback URL could not be parsed")

    # Check same‑domain or allowed domain
    if (
        callback_domain != parsed_host.hostname
        and callback_domain not in ALLOWED_CALLBACK_DOMAINS
    ):
        raise ValueError(
            f"Disallowed callback domain: {callback_domain}. "
            "Only same‑domain or domains in ALLOWED_CALLBACK_DOMAINS are permitted."
        )

    # Append the state parameter securely
    query = urllib.parse.parse_qs(parsed_full.query)
    query["state"] = [session_id]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL
    safe_url = urllib.parse.urlunparse(
        (
            parsed_full.scheme,
            parsed_full.netloc,
            parsed_full.path,
            parsed_full.params,
            new_query,
            parsed_full.fragment,
        )
    )

    return safe_url