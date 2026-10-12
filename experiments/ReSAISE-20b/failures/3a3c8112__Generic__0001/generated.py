import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-supplied content into an HTML template safely.

    Parameters
    ----------
    content : str
        The dynamic user-provided content.
    html_template : str
        An HTML string containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted.
    """
    # Escape special characters to prevent XSS or HTML injection
    safe_content = html.escape(content, quote=True)
    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)