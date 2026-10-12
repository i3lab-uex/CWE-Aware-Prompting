import html

# Predefined HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML page embedding the user-provided content safely.

    Parameters
    ----------
    visitor_content : str
        Content supplied by the user that will be inserted into the HTML page.

    Returns
    -------
    str
        The complete HTML document with the escaped user content.
    """
    # Escape any special HTML characters to prevent XSS or injection attacks.
    safe_content = html.escape(visitor_content, quote=True)

    # Fill the template with the safely escaped content.
    return html_template.format(user_content=safe_content)