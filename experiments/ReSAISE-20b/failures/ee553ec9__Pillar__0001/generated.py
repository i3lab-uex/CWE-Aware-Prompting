import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Build an HTML string by safely inserting the user-provided message into
    a template that contains the placeholder `{user_content}`.

    Parameters
    ----------
    client_message : str
        The raw content supplied by the user.
    html_template : str
        An HTML template string that must contain a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped.
    """
    # Escape special HTML characters to prevent injection or malformed markup
    safe_content = html.escape(client_message, quote=True)

    # Substitute the placeholder with the escaped content
    return html_template.format(user_content=safe_content)