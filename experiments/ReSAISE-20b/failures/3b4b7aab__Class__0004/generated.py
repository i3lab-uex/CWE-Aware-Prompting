import urllib.parse
from typing import Iterable

# Example list of allowed callback domains. In a real application this would be
# configurable and probably loaded from environment variables or a secure store.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str,
) -> str:
    """
    Build a fully-qualified OAuth callback URL that is safe for use in third‑party
    authentication flows.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://app.example.com").
    callback_uri : str
        The path that the OAuth provider should redirect to (e.g., "/oauth/callback").
    session_state : str
        A unique value that will be added as a query parameter to the callback URL.
        It is used to validate that the response corresponds to the original request.

    Returns
    -------
    str
        A fully qualified URL that includes the domain, path and a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure root_url ends with a slash so that urljoin behaves correctly
    if not root_url.endswith("/"):
        root_url += "/"

    # Join the base URL with the callback path
    joined = urllib.parse.urljoin(root_url, callback_uri)

    # Parse the URL components for further manipulation
    parsed = urllib.parse.urlparse(joined)

    # Normalise the domain (lowercase, strip port if present)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Remove default ports for comparison
    if ":" in parsed.netloc:
        host_part, port = parsed.netloc.split(":", 1)
        hostname = host_part.lower()

    if hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback domain '{hostname}' is not allowed")

    # Add the state parameter to the query string
    query = urllib.parse.parse_qs(parsed.query)
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the final URL
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url