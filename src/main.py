from textnode import TextNode, TextType
from generate_content import generate_page, generate_pages_recursive
import os
import shutil
import sys

STATIC_DIR = "./static"
PUBLIC_DIR = "./docs"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv)>1 else "/"
    
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.mkdir(PUBLIC_DIR)
    
    copy_dir(STATIC_DIR, PUBLIC_DIR)
    
    #generate_page(f"{CONTENT_DIR}/index.md", TEMPLATE_PATH, f"{PUBLIC_DIR}/index.html")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR, basepath)
    
def copy_dir(src: str, dst: str):
    dir_contents = [os.path.join(src, name) for name in os.listdir(src)]
    for content in dir_contents:
        if os.path.isfile(content):
            print(f"Copying file {content} -> {dst}")
            shutil.copy(content, dst)
        else:
            new_dst = os.path.join(dst, os.path.basename(content))
            print(f"Copying directory {content} -> {new_dst}")
            os.mkdir(new_dst)
            copy_dir(content, new_dst)

if __name__ == "__main__":
    main()