import html

def generate_html_response(user_content: str, *, html_template: str) -> str:
    """
    Generate an HTML page by embedding user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The raw text supplied by the user.
    html_template : str
        A template string containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML page with the user content safely escaped.
    """
    # Escape special characters to prevent XSS attacks
    safe_content = html.escape(user_content, quote=True)

    # Safely format the template with the escaped content
    return html_template.format(user_content=safe_content)