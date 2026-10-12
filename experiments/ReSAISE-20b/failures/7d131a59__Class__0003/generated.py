import urllib.parse
from typing import Set

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add other approved domains here.
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_path : str
        The relative path that the OAuth provider should redirect to
        (e.g., "/oauth/callback").
    state : str
        A unique, unguessable string used to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS`` or if the callback path contains a scheme.
    """
    # 1. Ensure that the callback_path is relative (no scheme or netloc).
    parsed_callback = urllib.parse.urlparse(callback_path)
    if parsed_callback.scheme or parsed_callback.netloc:
        raise ValueError(
            "callback_path must be a relative path without scheme or host"
        )

    # 2. Join base_url and callback_path safely.
    joined = urllib.parse.urljoin(base_url.rstrip("/") + "/", parsed_callback.path)

    # 3. Append the state query parameter.
    url_parts = list(urllib.parse.urlparse(joined))
    # Preserve existing query parameters if any.
    qs = urllib.parse.parse_qs(url_parts[4], keep_blank_values=True)
    qs["state"] = [state]
    url_parts[4] = urllib.parse.urlencode(qs, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # 4. Validate that the host is allowed.
    host = urllib.parse.urlparse(final_url).hostname
    if not host or host.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback URL host '{host}' is not allowed")

    return final_url