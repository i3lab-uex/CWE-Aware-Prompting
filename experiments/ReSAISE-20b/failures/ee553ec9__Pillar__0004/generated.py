import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Safely embed a user-provided message into an HTML template.

    Parameters
    ----------
    client_message : str
        The content contributed by a user.
    html_template : str
        An HTML structure containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The resulting HTML string with the user content inserted.
    """
    # Escape any potentially dangerous characters to prevent XSS or
    # breaking the HTML structure.
    safe_content = html.escape(client_message, quote=True)

    # Replace the placeholder with the escaped content.
    return html_template.replace("{user_content}", safe_content)