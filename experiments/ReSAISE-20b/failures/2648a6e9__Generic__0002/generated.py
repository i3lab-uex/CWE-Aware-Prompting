import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Insert user-provided content into an HTML template safely.

    Parameters
    ----------
    input_text : str
        Text contributed by the user.
    html_template : str
        HTML structure containing a placeholder `{user_content}`.

    Returns
    -------
    str
        The resulting HTML string with the user content inserted.
    """
    # Escape any special characters to prevent XSS
    safe_content = html.escape(input_text, quote=True)
    # Replace the placeholder with the escaped content
    return html_template.replace("{user_content}", safe_content)