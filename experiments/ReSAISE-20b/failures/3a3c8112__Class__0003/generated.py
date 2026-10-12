import html

# Example template (in real usage this would be passed or loaded from a file)
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
    Injects user-supplied content into an HTML template after escaping.

    Args:
        content (str): Dynamic user input to be inserted into the HTML.

    Returns:
        str: The final HTML string with escaped user content.
    """
    # Escape the user content to prevent XSS and injection attacks
    safe_content = html.escape(content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)