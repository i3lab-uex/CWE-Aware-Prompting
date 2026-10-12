import urllib.parse
from typing import Iterable

# Example list of allowed callback domains. In a real application this should be
# loaded from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}


def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_endpoint : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    verification_state : str
        A unique value to be appended as a query parameter for state validation.

    Returns
    -------
    str
        The complete callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL has a scheme; otherwise urljoin will treat it as relative.
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        raise ValueError(f"Base URL must include a scheme (http:// or https://): {app_base_url}")

    # Build the callback path relative to the base URL.
    joined = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", callback_endpoint.lstrip("/"))

    # Append the state parameter safely.
    url_parts = list(urllib.parse.urlparse(joined))
    query_dict = urllib.parse.parse_qs(url_parts[4])
    query_dict["state"] = [verification_state]
    url_parts[4] = urllib.parse.urlencode(query_dict, doseq=True)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate domain.
    netloc = urllib.parse.urlparse(final_url).netloc
    # Strip port if present.
    domain = netloc.split(":")[0]
    if domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not allowed for OAuth callbacks.")

    return final_url