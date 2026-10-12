import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Safely embed `client_message` into `html_template`.

    Parameters
    ----------
    client_message : str
        User-provided content to be inserted into the template.
    html_template : str
        HTML structure containing a `{user_content}` placeholder.

    Returns
    -------
    str
        The template with the user content safely escaped and inserted.
    """
    # Escape special HTML characters to prevent injection
    safe_content = html.escape(client_message, quote=True)

    # Ensure the placeholder exists in the template
    if "{user_content}" not in html_template:
        raise ValueError("Template must contain a '{user_content}' placeholder.")

    return html_template.replace("{user_content}", safe_content)