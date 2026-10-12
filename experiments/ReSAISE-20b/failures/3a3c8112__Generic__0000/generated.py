import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-supplied content into an HTML template safely.

    Parameters
    ----------
    content : str
        The dynamic content provided by the user.
    html_template : str
        A string representing the HTML structure. It must contain a single
        placeholder `{user_content}` where the escaped content will be inserted.

    Returns
    -------
    str
        The final HTML string with the escaped user content embedded.
    """
    # Escape special characters to prevent XSS attacks
    safe_content = html.escape(content, quote=True)
    return html_template.format(user_content=safe_content)