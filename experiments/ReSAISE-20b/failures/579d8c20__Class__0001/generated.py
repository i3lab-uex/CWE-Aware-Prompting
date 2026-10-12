import html

# Basic HTML template with a placeholder for user content.
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
    Construct an HTML page embedding the provided visitor content safely.

    Args:
        visitor_content: User supplied string to be inserted into the page.

    Returns:
        A complete HTML document with the user content escaped.
    """
    # Escape special HTML characters to prevent injection attacks (CWE-74).
    safe_content = html.escape(visitor_content, quote=True)
    # Render the final HTML.
    return html_template.format(user_content=safe_content)

# Example usage:
if __name__ == "__main__":
    user_input = "<script>alert('XSS');</script>"
    print(create_html_response(user_input))