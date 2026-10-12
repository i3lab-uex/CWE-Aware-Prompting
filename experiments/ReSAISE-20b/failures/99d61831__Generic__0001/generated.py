import html

def create_html_output(input_content: str, html_template: str) -> str:
    """
    Injects user-supplied content into an HTML template after escaping it.

    Parameters
    ----------
    input_content : str
        The dynamic content provided by the user.
    html_template : str
        An HTML string containing a placeholder `{user_content}`.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted.
    """
    # Escape the user-provided content to prevent XSS attacks
    escaped_content = html.escape(input_content, quote=True)

    # Safely format the template with the escaped content
    return html_template.format(user_content=escaped_content)