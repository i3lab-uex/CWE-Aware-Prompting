import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <!-- User content will be inserted below -->
    <div id="user-content">{user_content}</div>
</body>
</html>
"""

def construct_html_response(content: str) -> str:
    """
    Construct a safe HTML response by escaping user-provided content
    and injecting it into the predefined template.

    Args:
        content: Raw string supplied by the user that should appear
                 in the final HTML.

    Returns:
        A fully formed HTML string with the escaped user content.
    """
    # Escape special HTML characters to prevent injection attacks
    safe_content = html.escape(content, quote=True)

    # Ensure the template contains the placeholder before formatting
    if "{user_content}" not in html_template:
        raise ValueError("HTML template does not contain the required placeholder.")

    # Inject the escaped content into the template
    return html_template.format(user_content=safe_content)