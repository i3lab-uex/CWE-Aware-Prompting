import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Message</title>
</head>
<body>
    <h1>Welcome Visitor!</h1>
    <div class="message">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_page(visitor_message: str) -> str:
    """
    Render an HTML page by safely embedding the visitor's message into a
    predefined template.

    Parameters:
        visitor_message (str): The raw content contributed by the user.

    Returns:
        str: The final HTML string with the user's message inserted.
    """
    # Escape special characters to prevent XSS attacks
    safe_message = html.escape(visitor_message)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_message)