import sys
import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# The one page html file that makes up the blog
html_file = "/Users/bernie/Documents/my_files_at_work/logging/simpleblog.html"
blog_dir = Path("/Users/bernie/Documents/my_files_at_work/logging")
aws_bucket = "s3://berniemichalik.com"
aws_command = "aws s3 cp simpleblog.html s3://berniemichalik.com"

# Check for correct number of arguments
if len(sys.argv) < 3:
    print("Usage: python update_html.py 'MMMMMMM DD,YYYY' 'TEXT' ['IMAGE_URL' or 'FILE']")
    date_input = input("Enter the date (no quotes): ")
    text_input = input("Enter the log entry (no quotes): ")
    
    # Ask if user wants to add an image
    image_choice = input("Do you want to add an image? (url/file/none): ").strip().lower()
    
    image_url = None
    local_file = None
    
    if image_choice == "url":
        image_url = input("Enter the image URL: ").strip()
    elif image_choice == "file":
        filename = input("Enter the filename.ext (will look in Downloads): ").strip()
        downloads_dir = Path.home() / "Downloads"
        file_path = downloads_dir / filename
        
        if file_path.exists():
            print(f"✓ Found file: {file_path}")
            local_file = file_path
        else:
            print(f"✗ File not found in Downloads: {filename}")
            print(f"  Looked in: {downloads_dir}")
            sys.exit(1)
else:
    date_input = sys.argv[1]
    text_input = sys.argv[2]
    
    if len(sys.argv) > 3:
        third_arg = sys.argv[3]
        # Check if it's a URL (starts with http) or a file
        if third_arg.startswith("http"):
            image_url = third_arg
            local_file = None
        else:
            # Treat as filename
            downloads_dir = Path.home() / "Downloads"
            file_path = downloads_dir / third_arg
            
            if file_path.exists():
                print(f"✓ Found file: {file_path}")
                local_file = file_path
                image_url = None
            else:
                print(f"✗ File not found in Downloads: {third_arg}")
                sys.exit(1)
    else:
        image_url = None
        local_file = None

# Load the existing HTML file
try:
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
except FileNotFoundError:
    print(f"Error: '{html_file}' not found.")
    sys.exit(1)

# Find the container div
container = soup.find("div", class_="container")
if not container:
    print("Error: Could not find container div in the HTML file.")
    sys.exit(1)

# Create a new row div
new_row = soup.new_tag("div", **{"class": "row"})

# Create the date div
date_div = soup.new_tag("div", **{"class": "date"})
date_div.string = date_input

# Create the text div
text_div = soup.new_tag("div", **{"class": "text"})

# Add image if provided (either URL or local file)
if image_url:
    img_tag = soup.new_tag("img", src=image_url)
    text_div.append(img_tag)
elif local_file:
    # Use just the filename for the img src
    img_tag = soup.new_tag("img", src=local_file.name)
    text_div.append(img_tag)

# Add the paragraph text
paragraph = soup.new_tag("p")
paragraph.string = text_input
text_div.append(paragraph)

# Append date and text to the row
new_row.append(date_div)
new_row.append(text_div)

# Insert the new row at the top of the container
first_row = container.find("div", class_="row")
if first_row:
    first_row.insert_before(new_row)
else:
    container.append(new_row)

# Save the updated HTML back to the file
with open(html_file, "w", encoding="utf-8") as file:
    file.write(soup.prettify())

# Print confirmation message
if image_url:
    print(f"Added new entry with date '{date_input}', text '{text_input}', and image URL '{image_url}' to {html_file}.")
elif local_file:
    print(f"Added new entry with date '{date_input}', text '{text_input}', and image file '{local_file.name}' to {html_file}.")
else:
    print(f"Added new entry with date '{date_input}', text '{text_input}' to {html_file}.")

upload = input("Enter Y if you want to upload the blog now: ")

if upload == "Y":
    # Upload the HTML file
    os.system(aws_command)
    
    # If there's a local file, copy and upload it too
    if local_file:
        # Copy the file to the logging directory
        dest_file = blog_dir / local_file.name
        
        print(f"Copying {local_file.name} to {blog_dir}...")
        shutil.copy2(local_file, dest_file)
        
        # Upload the image file to S3
        print(f"Uploading {local_file.name} to S3...")
        os.system(f"aws s3 cp {dest_file} {aws_bucket}")
        
        print(f"✓ Successfully uploaded both HTML and {local_file.name}")
    else:
        print("✓ Successfully uploaded HTML")
