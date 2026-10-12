import html

# The base HTML structure with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 2rem;}
        .message-box {border: 1px solid #ccc; padding: 1rem; background:#f9f9f9;}
    </style>
</head>
<body>
    <h1>Visitor Message</h1>
    <div class="message-box">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Safely embed a visitor's message into the HTML template.

    Args:
        visitor_message: The raw text provided by a user.

    Returns:
        A string containing the complete HTML page with the message inserted.
    """
    # Escape any HTML special characters to prevent injection attacks.
    safe_content = html.escape(visitor_message)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)