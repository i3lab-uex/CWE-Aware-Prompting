import html

def create_html_output(input_content: str, html_template: str) -> str:
    """
    Safely inject user-provided content into an HTML template.

    Parameters
    ----------
    input_content : str
        The dynamic content supplied by the user.
    html_template : str
        An HTML structure containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped.
    """
    # Escape special characters to prevent injection attacks
    safe_content = html.escape(input_content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)