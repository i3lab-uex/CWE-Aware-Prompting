import html

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML response by inserting the user-provided content into a
    predefined template. The function safely escapes any HTML special characters
    in the user input to prevent script injection and other content‑injection
    attacks.

    Args:
        visitor_content (str): The raw user-provided content that will be
                               embedded into the HTML response.

    Returns:
        str: The final HTML string with the escaped user content inserted.
    """
    # Basic HTML template with a placeholder for user content
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome Visitor!</h1>
    <div id="content">{user_content}</div>
</body>
</html>"""

    # Escape the user content to neutralize any HTML/JS that could be injected.
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)