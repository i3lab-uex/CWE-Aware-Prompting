import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-supplied content into an HTML template safely.

    Parameters
    ----------
    content : str
        The dynamic user-provided content to be inserted.
    html_template : str
        A string containing the HTML structure. It must contain a single placeholder
        `{user_content}` where the escaped content will be placed.

    Returns
    -------
    str
        The final HTML string with the user content safely escaped.
    """
    # Escape special characters to prevent XSS attacks
    safe_content = html.escape(content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)