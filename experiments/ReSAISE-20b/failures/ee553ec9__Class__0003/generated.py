import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Insert the client message into an HTML template safely.

    Parameters
    ----------
    client_message : str
        Content provided by the user.
    html_template : str
        HTML structure containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the user content inserted.
    """
    # Escape special characters to prevent injection attacks (CWE‑74)
    safe_content = html.escape(client_message, quote=True)

    # Use format to insert the escaped content
    return html_template.format(user_content=safe_content)