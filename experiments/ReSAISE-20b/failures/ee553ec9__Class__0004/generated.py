import html

def build_html_output(client_message: str, html_template: str) -> str:
    """
    Build an HTML string by safely inserting user content into a template.

    Parameters
    ----------
    client_message : str
        The raw text supplied by the user that will be embedded in the HTML.
    html_template : str
        The template string containing a `{user_content}` placeholder.

    Returns
    -------
    str
        A fully formed HTML string with the user content safely escaped.
    """
    # Escape any special characters to prevent XSS or injection attacks
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)