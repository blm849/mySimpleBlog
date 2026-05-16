# My Simpleblog 

### Introduction

I wanted to go back to the very beginning of blogging, where someone’s blog could consist of just a simple html page with maybe some images to go along with it. But I also wanted to have an easy way to update it. The result can be see here: https://berniemichalik.com/simpleblog.html

The blog is a simple HTML file: **simpleblog.html**. Since I want to included some of my own images on the blog, there are jpegs that go along with it. I’ve provided one here **20260516-1.jpeg** just to show how it works. You don’t need to use images if you don’t want to.

### Updating simpleblog.html manually

Several times a week I edit simpleblog.html, save it, and upload it to an S3 bucket in AWS. This bucket is set up to act as a web site. If you need help with that, do a web search: “how to make an s3 bucket a web site”. I think this is a good guide: https://dev.to/naamiahmed/how-to-host-a-static-website-on-aws-s3-complete-step-by-step-guide-4cgf but feel free to approach it however you want. (Or just keep it local for now and don’t worry about hosting it online.)

To adopt simpleblog.html for your own uses, you want to change the following rows in it: 

```
- simpleblog.html: row 6: can change the title to whatever you want 
- simpleblog.html: row 13: These are the google fonts I use - feel free to swap these out. Go here for more examples of google fonts: https://fonts.google.com/    
- simpleblog.html: row 17:  This is a more complex version of the font I actually use to give me the date in bold and the text unbolded. Feel free to ignore or give it a try.
- simpleblog.html: row 22:  To keep it simple, I include my CSS right in the HTML file. Feel free to change out the background terrazzo image and the hero background image by going to those sites and looking for something better. Of course if you are comfortable with CSS, do as many different things as you want. 
- simpleblog.html: row 103: Each row of your blog sits within this container 
- simpleblog.html: row 105: Here is one blog row entry. You see the date, an image, and a blog entry as a paragraph 
- simpleblog.html: row 106: my images tend to use a naming convention of date-number since all images go in the same bucket and I don't want to overwrite new images over old ones. 
- simpleblog.html: row 119: Here is a second entry. Note there is no image 
```

Make those changes, file the html file, and then open the file with your browser to make sure it looks good. Then you can upload it to your S3 bucket and view it from the web. (__Note:__ you do NOT have to upload it at all. You can limit it to sitting on your computer if that’s what you prefer.)

### Updating simpleblog.html with simpleblog.py

If you are comfortable with python, you can update the blog with the program **simpleblog.py**. First you will want to go into the program and edit the values for these four variables at the top of the program

```
html_file = "/Users/bernie/Documents/my_files_at_work/logging/simpleblog.html"
blog_dir = Path("/Users/bernie/Documents/my_files_at_work/logging")
aws_bucket = "s3://berniemichalik.com"
aws_command = "aws s3 cp simpleblog.html s3://berniemichalik.com"
```

Then you can run the program simply by entering: 
```python simpleblog.py```

Here are two examples. In this example, I don’t have an image to upload. I just provide the date and my log entry and tell the program to upload it to my S3 bucket.
```
% python simpleblog.py
Usage: python simpleblog.py 'MMMMMMM DD,YYYY' 'TEXT' ['IMAGE_URL' or 'FILE']
Enter the date (no quotes): May 16, 2026
Enter the log entry (no quotes): Test with no image
Do you want to add an image? (url/file/none): none
Added new entry with date 'May 16, 2026', text 'Test with no image' to /Users/bernie/Documents/my_files_at_work/logging/simpleblog.html.
Enter Y if you want to upload the blog now: Y
upload: ./simpleblog.html to s3://berniemichalik.com/simpleblog.html
✓ Successfully uploaded HTML
% 
```
Here is the second example:

```
bernie@Bernies-MBP logging % python3 simpleblog.py
Usage: python simpleblog.py 'MMMMMMM DD,YYYY' 'TEXT' ['IMAGE_URL' or 'FILE']
Enter the date (no quotes): May 16, 2026
Enter the log entry (no quotes): Have started doing some drawing lately and trying out different material
Do you want to add an image? (url/file/none): file
Enter the filename.ext (will look in Downloads): 20260516-1.jpeg
✓ Found file: /Users/bernie/Downloads/20260516-1.jpeg
Added new entry with date 'May 16, 2026', text 'Have started doing some drawing lately and trying out different material', and image file '20260516-1.jpeg' to /Users/bernie/Documents/my_files_at_work/logging/simpleblog.html.
Enter Y if you want to upload the blog now: Y
upload: ./simpleblog.html to s3://berniemichalik.com/simpleblog.html
Copying 20260516-1.jpeg to /Users/bernie/Documents/my_files_at_work/logging...
Uploading 20260516-1.jpeg to S3...
upload: ./20260516-1.jpeg to s3://berniemichalik.com/20260516-1.jpeg
✓ Successfully uploaded both HTML and 20260516-1.jpeg
bernie@Bernies-MBP logging % 
```
In this second example, I have preloaded an image in my Mac’s Downloads directory. (If you want to have a different directory, you’ll have to modify the code. :)) I then run the code as before, but now instead of saying __none__ I say __file__ and then give it the name of the file (jpeg) to use.

What’s nice about using the program is that it always puts the latest entry at the top of the simpleblog.html. It keeps the blog in chronological order, from newest to oldest. Also the program is good if you don’t want to fuss with the HTML, since the program does that for you.

### Notes
1) If there is an image on the web you want to use, you can enter __url__ instead of __file__ and it will include that in your blog.

2) You can use the program like this: 
```python simpleblog.py 'MMMMMMM DD,YYYY' 'TEXT' ['IMAGE_URL' or 'FILE’]```
which is simple and not interactive. I like the interactive approach: I make less mistakes that way.

3) You do not have to automatically upload the simpleblog.html file to the S3 bucket. You can say __N__ when it asks you to upload and it will simply save your updates. Later you can use the shell script __upload.sh__ to upload the file later. (__Note:__ you will have to change upload.sh to point to your bucket.)

