import html

def create_html_output(input_text: str, html_template: str) -> str:
    """
    Safely embed user-provided content into an HTML template.

    Parameters
    ----------
    input_text : str
        Text supplied by the user to be inserted into the template.
    html_template : str
        The HTML structure containing a `{user_content}` placeholder.

    Returns
    -------
    str
        A new HTML string with the user content safely escaped.
    """
    # Escape special HTML characters to prevent injection (CWE‑74)
    safe_content = html.escape(input_text, quote=True)

    # Use str.format_map for safer placeholder replacement
    return html_template.format_map({"user_content": safe_content})