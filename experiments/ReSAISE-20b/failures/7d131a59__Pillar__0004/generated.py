import urllib.parse
from typing import Set

# Example set of allowed callback domains; in real code this would come from config
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a full OAuth callback URL and ensure it is hosted on an allowed domain.

    Args:
        base_url: The application's base URL (e.g., "https://myapp.com").
        callback_path: Path for the OAuth callback (e.g., "/oauth/callback").
        state: A unique state token used for CSRF protection.

    Returns:
        The fully-qualified callback URL including the `state` query parameter.

    Raises:
        ValueError: If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure base_url ends with a slash to allow proper joining
    if not base_url.endswith("/"):
        base_url += "/"

    # Join the base URL with the callback path
    full_path = urllib.parse.urljoin(base_url, callback_path.lstrip("/"))

    # Parse the URL to manipulate query parameters safely
    parsed = urllib.parse.urlparse(full_path)

    # Add the state parameter to existing query string (if any)
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # Overwrite or add the state parameter
    query_params["state"] = [state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate the domain against allowed domains
    hostname = urllib.parse.urlparse(final_url).hostname or ""
    # Strip leading 'www.' if present for comparison
    cleaned_host = hostname.lower().lstrip("www.")
    if cleaned_host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {cleaned_host}")

    return final_url