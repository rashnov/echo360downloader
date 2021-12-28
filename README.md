# echo360downloader
Downloads echo360 lectures

## How to fill in the cookie.txt file
Log in to echo360 with the developer console open on "Network".
Onced logged in click on one of the get requests such as the one for enrollments and copy the cookie starting at ECHO_JWT to the end and paste it into the
cookie file.

Run the program using python main.py to download every lecture into course coded folders in the current directory.
