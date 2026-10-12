import urllib.parse
from typing import Set

# Example set of allowed callback domains. In real usage this should be
# configured from a secure source (e.g., environment variable or config file).
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.myapp.org"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://myapp.com").
    path_callback : str
        The endpoint for the OAuth callback (e.g., "/auth/callback").
    session_id : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with a state query parameter.

    Raises
    ------
    ValueError
        If the callback URL domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the host's domain.
    """
    # Normalise the base URL to avoid double slashes
    base = host_url.rstrip("/")
    callback_path = path_callback.lstrip("/")

    # Construct the full callback URL
    raw_url = f"{base}/{callback_path}"
    parsed = urllib.parse.urlparse(raw_url)

    # Validate the domain
    host_domain = urllib.parse.urlparse(host_url).hostname or ""
    callback_domain = parsed.hostname or ""

    if not callback_domain:
        raise ValueError("Callback URL must contain a valid hostname")

    # Allow same‑domain callbacks or domains explicitly listed
    if callback_domain != host_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter (URL‑encoded)
    query = urllib.parse.urlencode({"state": session_id})
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment,
        )
    )

    return final_url