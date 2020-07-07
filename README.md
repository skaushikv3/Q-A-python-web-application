# Q-A-python-web-application
 This is Question and answering platform. Users can post question, answer to own and other question. guest users can view to questions. This application uses flask as backend server to run the web page

## Installation
 python package requirments
 ```python
 pip install flask
 pip install sqlite3
 ```
 (in code)
 ```
 from flask import Flask, session, redirect, url_for, request,render_template, jsonify
 import sqlite3 
 ```
 user interface requirements (website like to get started)
 ```
 [jquery][https://getbootstrap.com/docs/4.3/getting-started/download/]
 [bootstrap][https://getbootstrap.com/docs/4.3/getting-started/download/]
 [font-awsome][https://fontawesome.com/v4.7.0/get-started/]
 ```
 
## deployed location [website](http://kaushiks.pythonanywhere.com/)
 
## language
 Python 3.7 is the programming language
## database
 sqlite3 is the database
## front end
 html, javascript, bootstrap, ajax, css is used
 
 ## functions
  
   A user can sign up with (username,email,password) 
   
   on launch on the page, the application shows all the post in the decending order of posted time.
   
   upon user login the create post and view user post will be visible.
   
   the search bar can be used to search a keyword against the post titel or post description
   
   edit and delit option will be visible upon login to the post or answer posted by the logined user.
   
   the posted by name in post and in answer can be used to search the respective username or tag and results will be shown accordingly
   
   
   
   
