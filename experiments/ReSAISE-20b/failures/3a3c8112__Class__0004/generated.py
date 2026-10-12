import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Injects user-supplied content into an HTML template safely.

    Parameters
    ----------
    content : str
        The dynamic user-provided content to be inserted.
    html_template : str
        An HTML template containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped.
    """
    # Escape special characters to prevent injection attacks (CWE-74)
    safe_content = html.escape(content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)