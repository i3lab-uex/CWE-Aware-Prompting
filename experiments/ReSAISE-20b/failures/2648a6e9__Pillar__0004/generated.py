import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Insert user-provided content into an HTML template safely.

    Parameters
    ----------
    input_text : str
        The raw content supplied by the user.
    html_template : str
        An HTML string containing a single placeholder `{user_content}`.

    Returns
    -------
    str
        The HTML string with the user content inserted after escaping.
    """
    # Escape special characters to prevent injection attacks
    safe_content = html.escape(input_text, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)