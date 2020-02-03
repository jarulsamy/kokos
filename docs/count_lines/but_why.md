## Why to make something like this?
Here are some examples of where this could be useful:
* Statistics
* Tracking the progress of a project (see [measuring_work_in_lines_of_code.md](measuring_work_in_lines_of_code.md))
* "Just for fun"

## "You can write it in like 5 lines of code"
Many people will be confused about why did I took the time to write such a
complex program only to get a few numbers out of it. The answer is that its
not so easy as to:
* Read a file
* Split it where there is a new line
* Get the number of lines

In the theory, yes its 5 lines of code but in practice its way harder:
* Read all the files inside a directory (including files in sub-folders)
* Exclude all files with an extension in **exclude_ext** or name in **exclude_files**
* Exclude all folders with a name in **exclude_folders**
* Split it where there is a new line
* For every line check:
* * If its a comment. This depends on the file extension and **comment_prefixes**.
* * If its blank
* Organize number of lines per extension type and in total
* Optimizing speed
* Error handling
