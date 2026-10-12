import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Page</title>
</head>
<body>
    <!-- User supplied content will appear below -->
    <div id="content">{user_content}</div>
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Build a complete HTML page by injecting the supplied user content
    into a predefined template. The user content is properly escaped to
    prevent XSS and ensure the output remains well‑formed.

    Args:
        page_content: The raw string provided by the user.

    Returns:
        A fully formed HTML string with the escaped user content
        inserted into the template.
    """
    # Escape all special HTML characters in the user supplied content.
    escaped_content = html.escape(page_content, quote=True)

    # Insert the escaped content into the template.
    final_html = html_template.format(user_content=escaped_content)

    return final_html