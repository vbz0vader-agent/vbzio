import os
import re
from html.parser import HTMLParser

class LinkAndMetaValidator(HTMLParser):
    def __init__(self, base_path):
        super().__init__()
        self.base_path = base_path
        self.links = []
        self.title = None
        self.description = None
        self.in_title = False
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = None
            content = None
            for attr, value in attrs:
                if attr == 'name':
                    name = value
                elif attr == 'content':
                    content = value
            if name == 'description':
                self.description = content

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()

    def reset_data(self):
        self.links = []
        self.title = None
        self.description = None
        self.in_title = False
        self.errors = []
        self.reset()

def validate_file(filepath, base_path):
    validator = LinkAndMetaValidator(base_path)
    file_errors = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        validator.feed(content)

    # Validate Title and Description
    if not validator.title:
        file_errors.append(f"Missing or empty <title> tag in {filepath}")
    if not validator.description:
        file_errors.append(f"Missing or empty <meta name=\"description\"> tag in {filepath}")

    # Validate Links
    for link in validator.links:
        if link.startswith('/') and not link.startswith('//'):  # Absolute path relative to site root
            target_path = os.path.join(base_path, link[1:])
        elif not re.match(r'^(https?://|mailto:)', link):  # Relative path or local file
            target_path = os.path.join(os.path.dirname(filepath), link)
        else:  # External link or mailto, skip local validation
            continue

        if not os.path.exists(target_path) and not (link == '/' and os.path.exists(os.path.join(base_path, 'index.html'))):
            file_errors.append(f"Broken link '{link}' in {filepath}. Target '{target_path}' not found.")

    return file_errors

def main():
    base_path = os.getcwd()
    all_errors = []
    html_files = [f for f in os.listdir(base_path) if f.endswith('.html')]

    for html_file in html_files:
        filepath = os.path.join(base_path, html_file)
        errors = validate_file(filepath, base_path)
        all_errors.extend(errors)

    if all_errors:
        print("Validation FAILED:")
        for error in all_errors:
            print(f"- {error}")
        return 1
    else:
        print("Validation PASSED: All local links and metadata are valid.")
        return 0

if __name__ == "__main__":
    exit(main())
