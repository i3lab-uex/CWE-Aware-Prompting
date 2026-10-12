import html

def render_html_page(visitor_message: str, html_template: str) -> str:
    """
    Render an HTML page by safely inserting the visitor's message into a template.

    Parameters
    ----------
    visitor_message : str
        The content provided by the user to be inserted into the template.
    html_template : str
        An HTML string containing a single placeholder `{user_content}` where the
        visitor's message should appear.

    Returns
    -------
    str
        The final HTML string with the user content safely escaped and inserted.
    """
    # Escape any potentially dangerous characters to prevent XSS or HTML injection
    safe_content = html.escape(visitor_message, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_content)