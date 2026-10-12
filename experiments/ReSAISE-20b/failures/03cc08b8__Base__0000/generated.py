import re
from urllib.parse import urlparse, urljoin

# Example set of allowed callback domains. In real code this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback(application_url: str, callback_route: str, token_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g. "https://myapp.com").
    callback_route : str
        The relative path to the OAuth callback handler (e.g. "/auth/callback").
    token_state : str
        A unique state value used to protect against CSRF.

    Returns
    -------
    str
        The fully assembled OAuth callback URL, e.g.
        "https://myapp.com/auth/callback?state=abc123".

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS`` and does not match the base domain of
        ``application_url``.
    """
    if not application_url:
        raise ValueError("Application URL must be provided")
    if not callback_route:
        raise ValueError("Callback route must be provided")
    if not token_state:
        raise ValueError("Token state must be provided")

    # Ensure callback_route is a relative path (no scheme or netloc)
    parsed_cb = urlparse(callback_route)
    if parsed_cb.scheme or parsed_cb.netloc:
        raise ValueError("Callback route must be a relative path, not an absolute URL")

    # Construct the full callback URL
    base = application_url.rstrip("/")
    cb_path = parsed_cb.path.lstrip("/")  # remove leading slash to avoid double slashes
    full_url = f"{base}/{cb_path}"
    if parsed_cb.query:
        full_url += f"?{parsed_cb.query}"

    # Append the state parameter
    separator = "&" if "?" in full_url else "?"
    callback_with_state = f"{full_url}{separator}state={token_state}"

    # Validate the domain of the resulting URL
    callback_domain = urlparse(callback_with_state).netloc.lower()
    # Strip potential port numbers
    callback_domain = re.sub(r":\d+$", "", callback_domain)

    # Extract base domain from application_url for comparison
    app_netloc = urlparse(application_url).netloc.lower()
    app_domain = re.sub(r":\d+$", "", app_netloc)

    if callback_domain not in ALLOWED_CALLBACK_DOMAINS and callback_domain != app_domain:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain}. "
            "Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return callback_with_state