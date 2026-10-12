import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Build an HTML string by safely inserting user-provided content into a template.

    Parameters
    ----------
    client_message : str
        The raw user input that will be inserted into the HTML.
    html_template : str
        An HTML template containing a single placeholder `{user_content}`.

    Returns
    -------
    str
        The resulting HTML with the user content escaped to prevent injection.
    """
    # Escape special characters in the user message to avoid HTML injection
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)