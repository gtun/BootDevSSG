from markdown_to_html import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown:str):
    lines = markdown.split("\n")
    for line in lines:
        if line.split(" ", 1)[0] == "#":
            return line.split(" ", 1)[1].strip()
    raise ValueError("No h1 headings found")

def generate_page(from_path:str, template_path:str, dest_path:str, basepath:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        markdown_data = f.read()
    
    with open(template_path, encoding="utf-8") as f:
        template_data = f.read()
    
    html_string = markdown_to_html_node(markdown_data).to_html()
    
    title = extract_title(markdown_data)
    
    full_html = template_data.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
  
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath: str):
    dir_contents = os.listdir(dir_path_content)
    for content in dir_contents:
        if os.path.isfile(os.path.join(dir_path_content,content)):
            if Path(content).suffix == ".md":
                generate_page(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, Path(content).with_suffix(".html")), basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, content), basepath)