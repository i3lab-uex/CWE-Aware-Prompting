import urllib.parse

# Set of domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any other trusted domains here.
}

def assemble_oauth_callback_url(root_url: str, path_for_callback: str, session_token: str) -> str:
    """
    Construct a full OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://myapp.com").
    path_for_callback : str
        The relative path that handles the OAuth callback (e.g. "/auth/callback").
    session_token : str
        A token used as the `state` query parameter to protect against CSRF.

    Returns
    -------
    str
        The fully qualified callback URL including the `state` parameter.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the root URL: ensure it has a scheme and no trailing slash.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        raise ValueError(f"Root URL must include a scheme (http:// or https://): {root_url}")
    if not parsed_root.netloc:
        raise ValueError(f"Root URL must include a network location: {root_url}")

    # Build the absolute callback URL.
    joined = urllib.parse.urljoin(root_url.rstrip("/") + "/", path_for_callback.lstrip("/"))
    parsed_joined = urllib.parse.urlparse(joined)

    # Verify that the domain is authorised.
    if parsed_joined.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Unauthorized callback domain: {parsed_joined.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    # Append the state parameter safely.
    query_params = urllib.parse.parse_qs(parsed_joined.query)
    query_params["state"] = [session_token]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL.
    final_url = urllib.parse.urlunparse(
        (
            parsed_joined.scheme,
            parsed_joined.netloc,
            parsed_joined.path,
            parsed_joined.params,
            new_query,
            parsed_joined.fragment,
        )
    )

    return final_url