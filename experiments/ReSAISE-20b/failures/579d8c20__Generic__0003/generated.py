import html

# Basic HTML template with a placeholder for user content
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
    Construct an HTML page embedding the provided visitor content.

    The function escapes all characters that could be interpreted as
    markup to prevent cross‑site scripting (XSS) attacks.

    Parameters:
        visitor_content (str): User supplied content to embed in the page.

    Returns:
        str: The complete HTML response with safe user content inserted.
    """
    # Escape the visitor content to neutralise any embedded markup or scripts
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)