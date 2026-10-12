import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Insert the user-provided content into an HTML template safely.

    Parameters
    ----------
    input_text : str
        The content contributed by the user.
    html_template : str
        The HTML structure containing a placeholder `{user_content}`.

    Returns
    -------
    str
        The resulting HTML string with the user content embedded.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(input_text, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)