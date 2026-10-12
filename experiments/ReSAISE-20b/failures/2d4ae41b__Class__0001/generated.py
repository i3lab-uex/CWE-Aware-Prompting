import html

def render_html_page(visitor_message: str, html_template: str) -> str:
    """
    Render an HTML page by inserting the visitor's message into a template.

    Parameters
    ----------
    visitor_message : str
        The content contributed by the user.
    html_template : str
        An HTML template containing a single placeholder `{user_content}`.

    Returns
    -------
    str
        The rendered HTML with the user content safely escaped.
    """
    # Escape special characters to prevent XSS or injection attacks
    safe_message = html.escape(visitor_message, quote=True)

    # Replace the placeholder with the escaped content
    return html_template.format(user_content=safe_message)