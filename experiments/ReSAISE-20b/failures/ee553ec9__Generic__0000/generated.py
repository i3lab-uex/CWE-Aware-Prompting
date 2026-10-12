import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Build an HTML response by safely inserting the user's message into a template.

    Parameters
    ----------
    client_message : str
        The content contributed by the user.
    html_template : str
        An HTML string containing a `{user_content}` placeholder where the user's message will be inserted.

    Returns
    -------
    str
        The resulting HTML string with the user content escaped and embedded.

    Notes
    -----
    - `html.escape` is used to prevent injection of arbitrary HTML or JavaScript.
    - The function assumes that the template contains exactly one `{user_content}` placeholder.
    """
    # Escape special HTML characters to avoid injection attacks
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)