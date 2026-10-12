import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-provided content into an HTML template after escaping.

    Parameters
    ----------
    content : str
        The dynamic content supplied by the user.
    html_template : str
        The HTML template containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)