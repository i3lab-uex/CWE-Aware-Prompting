import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Safely inject user-provided content into an HTML template.

    Parameters
    ----------
    content : str
        The dynamic user-supplied content that will be inserted into the template.
    html_template : str
        The HTML structure containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The final HTML string with the user content properly escaped to prevent
        HTML injection attacks (CWE-74).
    """
    # Escape special characters in user content to neutralize potential injection
    safe_content = html.escape(content, quote=True)

    # Perform the placeholder substitution.  Use format to avoid accidental
    # formatting errors if the template contains other braces.
    return html_template.format(user_content=safe_content)