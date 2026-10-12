import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Insert the user-provided content into an HTML template safely.

    Parameters
    ----------
    client_message : str
        The raw text contributed by the user.
    html_template : str
        An HTML string containing a single placeholder `{user_content}` where
        the escaped user message should be inserted.

    Returns
    -------
    str
        The final HTML string with the user content embedded.
    """
    # Escape special HTML characters to prevent injection attacks
    escaped_message = html.escape(client_message, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=escaped_message)