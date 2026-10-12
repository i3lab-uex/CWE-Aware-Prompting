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
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML page by safely inserting the visitor's content
    into a predefined template.

    Parameters
    ----------
    visitor_content : str
        User supplied content that will be embedded into the page.

    Returns
    -------
    str
        The final HTML string with the user's content safely escaped.
    """
    # Escape special HTML characters to prevent injection (CWE-74).
    safe_content = html.escape(visitor_content, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)