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
    <!-- User supplied content goes here -->
    {user_content}
</body>
</html>
"""

def build_html_page(page_content: str) -> str:
    """
    Builds a complete HTML page by inserting escaped user content into the template.

    Args:
        page_content (str): Dynamic content supplied by a user.

    Returns:
        str: The final HTML string with the user content safely escaped.
    """
    # Escape special HTML characters to prevent injection attacks (CWE-78, CWE-79).
    safe_content = html.escape(page_content, quote=True)

    # Safely format the template. Using str.format is fine here because
    # we've already escaped user input; no other placeholders exist.
    final_html = html_template.format(user_content=safe_content)

    return final_html