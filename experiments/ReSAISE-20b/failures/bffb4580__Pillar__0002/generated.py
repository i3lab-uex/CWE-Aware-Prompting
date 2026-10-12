import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Page</title>
</head>
<body>
    <h1>Hello, User!</h1>
    <p>{user_content}</p>
</body>
</html>
"""

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page that safely embeds user-provided content.

    Args:
        client_input (str): Content supplied by the user to be inserted into
                            the HTML response.

    Returns:
        str: The complete HTML page with user content safely escaped to
             prevent script injection attacks.

    Raises:
        ValueError: If the placeholder `{user_content}` is missing from
                    `html_template`.  This ensures that the template
                    contains a valid insertion point.
    """
    # Ensure the placeholder exists in the template
    if "{user_content}" not in html_template:
        raise ValueError("Template missing '{user_content}' placeholder.")

    # Escape user input to neutralize any HTML or script tags
    safe_input = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_input)

# Example usage:
if __name__ == "__main__":
    user_str = '<script>alert("XSS")</script> Hello!'
    print(build_html_page(user_str))