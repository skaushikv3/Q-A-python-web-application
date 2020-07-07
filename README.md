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
 
 [jquery](https://getbootstrap.com/docs/4.3/getting-started/download/)
 [bootstrap](https://getbootstrap.com/docs/4.3/getting-started/download/)
 [font-awsome](https://fontawesome.com/v4.7.0/get-started/)
 
## deployed location [website](http://kaushiks.pythonanywhere.com/)
 
## features
```
1. Authentication
  a. Sign up - with email and password
  b. Sign in
  c. Sign out
```
```
2. Authorization
  a. Guests can view information available (including search).
  b. Registered users can create / update / delete a post.
  c. Updation / Deletion is restricted only to the creator of the post.
```
```
3. Question
  a. Registered users can create a question with title, description and tags.
  b. Title and Description are validated (can't be empty).
  c. Questions can be edited / deleted only by the creator.
  d. Questions are listed according to the date of creation (descending, with latest question on top).
  e. Questions can be searched based on the title / tags associated with them.
```
```
4. Answer
  a. Registered users can answer a question (even to their own question).
  b. Answers are listed while viewing each question, according to the date of
  creation (descending, with latest answer on top).
  c. Answers can be edited / deleted only by the creator.
```
## programming techenology stack

 ### Backed programming (server) 
   
   Python 3.7 [website](https://www.python.org/) [to get started Tutorial](https://www.w3schools.com/python/default.asp)

 ### Database (record storage)
   
   sqlite3 [website](https://www.sqlite.org/index.html) [to get started Tutorial for SQL](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)

 ### frontend programming (UI)
   
   HTML [to get started Tutorial](https://www.w3schools.com/html/)
   
   CSS [to get started Tutorial](https://www.w3schools.com/css/default.asp)
   
   BOOTSTRAP 4 [to get started Tutorial](https://www.w3schools.com/bootstrap4/default.asp)
   
   JQUERY [to get started Tutorial](https://www.w3schools.com/jquery/default.asp)
   
   JAVASCRIPT [to get started Tutorial](https://www.w3schools.com/js/default.asp)

   
   
