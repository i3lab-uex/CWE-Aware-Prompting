import html

# The HTML structure that will contain user supplied content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Content</title>
</head>
<body>
    <!-- User content will appear below -->
    <div id="content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Injects user-supplied content into an HTML template after escaping it
    to prevent injection attacks (CWE‑74).

    Args:
        input_content: The raw string provided by the user.

    Returns:
        A complete HTML document as a string with the escaped content
        inserted in place of the {user_content} placeholder.
    """
    # Escape special HTML characters to neutralize any injected markup or scripts
    safe_content = html.escape(input_content, quote=True)

    # Format the template with the escaped content
    return html_template.format(user_content=safe_content)