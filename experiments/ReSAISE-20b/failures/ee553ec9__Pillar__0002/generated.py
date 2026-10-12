import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Insert user-provided content into an HTML template safely.

    Parameters
    ----------
    client_message : str
        The raw text supplied by the user.
    html_template : str
        An HTML string containing a single placeholder `{user_content}` where the
        escaped user content should be inserted.

    Returns
    -------
    str
        The final HTML string with the user content safely embedded.
    """
    # Ensure the placeholder exists; raise a ValueError if not found
    if "{user_content}" not in html_template:
        raise ValueError("The provided template does not contain a '{user_content}' placeholder.")

    # Escape the user content to prevent XSS and other injection attacks
    escaped_content = html.escape(client_message, quote=True)

    # Perform a safe formatting operation
    return html_template.format(user_content=escaped_content)