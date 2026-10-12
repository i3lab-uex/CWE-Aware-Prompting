import html

def create_html_output(input_content: str, html_template: str) -> str:
    """
    Inject user-provided content into an HTML template safely.

    Parameters
    ----------
    input_content : str
        Dynamic content supplied by the user.
    html_template : str
        An HTML template containing the placeholder `{user_content}`.

    Returns
    -------
    str
        The final HTML string with the user content escaped to prevent injection.
    """
    # Escape special characters in the user content to avoid HTML injection
    safe_content = html.escape(input_content, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)