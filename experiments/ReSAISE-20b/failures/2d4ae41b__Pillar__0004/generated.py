import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="message">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page with the visitor's message safely embedded.

    Parameters
    ----------
    visitor_message : str
        The content contributed by a user that will be inserted into the HTML template.

    Returns
    -------
    str
        The resulting HTML string that includes the user’s content, properly escaped to prevent XSS.
    """
    # Escape special HTML characters in the user-provided message.
    safe_content = html.escape(visitor_message, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)