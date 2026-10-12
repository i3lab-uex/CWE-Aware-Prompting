import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Safely embed user-provided content into an HTML template.

    Args:
        client_message: The raw text supplied by the user.
        html_template: An HTML string containing a single `{user_content}` placeholder.

    Returns:
        A new HTML string with the user content properly escaped.
    """
    # Escape special characters to prevent injection attacks (CWE‑74)
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)