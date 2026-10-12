import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML page embedding the provided visitor content.

    Parameters
    ----------
    visitor_content : str
        The raw string supplied by the user that should be displayed in the page.

    Returns
    -------
    str
        The full HTML document with the user content safely escaped to prevent XSS.

    Notes
    -----
    The function uses :func:`html.escape` to encode special characters so that any
    embedded HTML or JavaScript is rendered as plain text rather than executed.
    """
    # Escape user content to avoid script injection
    safe_content = html.escape(visitor_content, quote=True)
    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)