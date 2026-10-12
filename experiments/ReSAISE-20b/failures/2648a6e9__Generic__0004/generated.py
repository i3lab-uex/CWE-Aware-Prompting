import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Insert user-provided content into an HTML template safely.

    Parameters
    ----------
    input_text : str
        Content contributed by a user.
    html_template : str
        HTML structure containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The resulting HTML string with the user content safely embedded.
    """
    # Escape any potentially dangerous characters in the user input
    safe_content = html.escape(input_text, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.replace("{user_content}", safe_content)