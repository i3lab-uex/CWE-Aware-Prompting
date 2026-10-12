import html

# Example template; in real usage this would be provided externally.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Response</title></head>
<body>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def construct_html_response(content: str) -> str:
    """
    Injects the user-provided content into an HTML template after escaping it.

    Args:
        content: The raw string supplied by the user that will be inserted into
                 the template.

    Returns:
        A complete HTML string with the escaped user content embedded.
    """
    # Escape special HTML characters to prevent XSS or markup injection
    escaped_content = html.escape(content, quote=True)
    # Insert the escaped content into the template
    return html_template.format(user_content=escaped_content)