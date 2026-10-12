import html

def create_html_output(input_content: str, html_template: str) -> str:
    """
    Injects the escaped user content into the given HTML template.

    Parameters
    ----------
    input_content : str
        The dynamic content supplied by the user.
    html_template : str
        A string containing an HTML structure with a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the user content safely escaped.
    """
    # Escape special characters to prevent XSS attacks
    safe_content = html.escape(input_content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)