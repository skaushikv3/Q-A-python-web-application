from flask import Flask, session, redirect, url_for, escape, request,render_template, jsonify, flash
import sqlite3
app = Flask(__name__)

location = ["index","myposts"] 
def secretkeygeneration():
    import secrets
    import string
    key=str(''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(16)))
    print('secret key: ',key)
    return key

#app.secret_key = secretkeygeneration()
def write_post(post_title,post_description,post_tag,user_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    #print(post_title,',',post_description,',',post_tag,',',user_id)
    try:
        mydb.execute('insert into questions (user_id,timestamp,title,description,tag) values (?,?,?,?,?);',[user_id,generate_timestamp(),post_title,post_description,post_tag])
        mydb.commit()
        mydb.close()
        return ('post entry sucessfull')
    except sqlite3.Error as error:
        print(error)
        return error

def update_post(post_title,post_description,post_tag,question_id,user_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    print(post_title,',',post_description,',',post_tag,',',question_id,',',user_id)
    try:
        mydb.execute("UPDATE questions set 'timestamp' = ? , 'title' = ? , 'description' = ? , 'tag'= ? where question_id = ? and user_id = ?",[generate_timestamp(),post_title,post_description,post_tag,question_id,user_id])
        mydb.commit()
        mydb.close()
        return ('sucessfull post update')
    except sqlite3.Error as error:
        print(error)
        return error    

def delete_post(question_id,user_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    print(question_id,',',user_id) 
    try:
        mydb.execute("DELETE FROM answers WHERE user_id = ? AND question_id = ?",[user_id,question_id])
        mydb.execute("DELETE FROM questions WHERE  user_id = ? AND question_id = ?",[user_id,question_id])
        mydb.commit()
        mydb.close()
        return ('sucessfull post delete')
    except sqlite3.Error as error:
        print(error)
        return error

def write_answer(answer,user_id,question_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    print(answer,',',user_id,',',question_id)
    try:
        mydb.execute('insert into answers (user_id,question_id,timestamp,answer) values (?,?,?,?);',[user_id,question_id,generate_timestamp(),answer])
        mydb.commit()
        mydb.close()
        return ('answer entry sucessfull')
    except sqlite3.Error as error:
        print(error)
        return error

def update_answer(answer,answer_id,user_id,question_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    #print(answer,',',answer_id,',',user_id,',',question_id)
    try:
        mydb.execute("UPDATE answers set 'answer' = ? , 'timestamp'=? where answer_id = ? and user_id = ? and question_id = ?",[answer,generate_timestamp(),answer_id,user_id,question_id])
        mydb.commit()
        mydb.close()
        return ('sucessfull answer update')
    except sqlite3.Error as error:
        print(error)
        return error
def generate_timestamp():
    import datetime
    return datetime.datetime.strptime((datetime.datetime.now()).strftime("%d-%b-%Y %H:%M:%S"), "%d-%b-%Y %H:%M:%S")

def collect_data_from_question(keyword):
    mydb = sqlite3.connect('server_data.db')
    if keyword != 'none':
        con = mydb.execute("SELECT  Q.question_id,A.username,Q.timestamp,Q.title, Q.description, Q.tag, Q.user_id FROM questions Q join authentication A on (Q.user_id == A.user_id) where Q.user_id = ? order by Q.timestamp DESC ;",[keyword])
        result= con.fetchall()
        mydb.close()
        return result
    else:
        con = mydb.execute("SELECT  Q.question_id,A.username,Q.timestamp,Q.title, Q.description, Q.tag, Q.user_id FROM questions Q join authentication A on (Q.user_id == A.user_id) order by Q.timestamp DESC ;")
        result= con.fetchall()
        mydb.close()
        return result

def delete_answer(answer_id,user_id,question_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    print(answer_id,',',user_id,',',question_id)
    try:
        mydb.execute("DELETE FROM answers WHERE answer_id = ? AND user_id = ? AND question_id = ?",[answer_id,user_id,question_id])
        mydb.commit()
        mydb.close()
        return ('sucessfull answer delete')
    except sqlite3.Error as error:
        print(error)
        return error

def collect_data_form_answers(question_id):
    mydb = sqlite3.connect('server_data.db')
    con = mydb.execute("SELECT A.answer_id,S.username, A.timestamp, A.answer, A.user_id FROM answers A join authentication S on (A.user_id ==S.user_id)  where question_id = ? order by timestamp DESC;",[question_id])
    result= con.fetchall()
    mydb.close()
    return result


def collect_data_from_question_by_userid(keyword):
    mydb = sqlite3.connect('server_data.db')
    if keyword != 'none':
        con = mydb.execute("SELECT  Q.question_id, A.username, Q.timestamp, Q.title, Q.description, Q.tag, Q.user_id FROM questions Q join authentication A on (Q.user_id == A.user_id) where Q.user_id = ? order by Q.timestamp DESC ;",[keyword])
        result= con.fetchall()
        mydb.close()
        return result
    else:
        con = mydb.execute("SELECT  Q.question_id, A.username, Q.timestamp, Q.title, Q.description, Q.tag, Q.user_id FROM questions Q join authentication A on (Q.user_id == A.user_id) order by Q.timestamp DESC ;")
        result= con.fetchall()
        mydb.close()
        return result

def collect_data_from_question_by_tag(keyword):
    print(keyword)
    mydb = sqlite3.connect('server_data.db')
    if keyword != 'none':
        con = mydb.execute("SELECT  Q.question_id, A.username, Q.timestamp, Q.title, Q.description, Q.tag, Q.user_id FROM questions Q join authentication A on (Q.user_id == A.user_id) where Q.tag = ? order by Q.timestamp DESC ;",[keyword])
        result= con.fetchall()
        mydb.close()
        return result


def gather_data1(session_id,select_key_location='none',select_key='none',search_key ='none'):
    check_scroll_height=lambda x : '0' if x==0 else '140'
    check_scroll_status=lambda x : 'hidden' if x==0 else 'scroll'
    check_edit_status=lambda x,y : 'inline-block' if x==y else 'none'
    post={'question_id':'','question postedby':'','question timestamp':'','question answer scroll status':'','question answer scroll height':'','question title':'','question description':'','question tag':'','no of answers':'','question answers':'','question edit_status':''}
    answers={'answer_id':'','answered by':'','answer timestamp':'','answer':'','answer edit_status':''}
    total_answers=[]
    # total_answers_f=[]
    total_post=[]
    if select_key_location =='none':
        question_data=collect_data_from_question_by_userid(select_key)
    elif select_key_location =='user_id':
        question_data=collect_data_from_question_by_userid(select_key)
    elif select_key_location =='tag_id':
        print('inside tag')
        question_data=collect_data_from_question_by_tag(select_key)
    if len(question_data) !=0:

        if search_key !='none':
            print('search key found')
            for q in question_data:
                total_answers.clear()
                if (q[3].count(search_key)>0) or (q[4].count(search_key)>0):
                    print('found a match')
                    answer_data=collect_data_form_answers(q[0])
                    print('----')
                    if len(answer_data)!=0:
                        for a in answer_data:
                            print('\n')
                            answers['answer_id']=a[0]
                            answers['answered by']=a[1]
                            answers['answer timestamp']=a[2]
                            answers['answer']=a[3]
                            answers['answer edit_status']=check_edit_status(session_id,a[4])
                            total_answers.append(answers.copy())
                            post['question answer scroll status']=check_scroll_status(len(answer_data))

                    post['question answer scroll height']=check_scroll_height(len(answer_data))
                    post['question edit_status']=check_edit_status(session_id,q[6])
                    post['question_id']=q[0]
                    post['question postedby']=q[1]
                    post['question timestamp']=q[2]
                    post['question title']=q[3]
                    post['question description']=q[4]
                    post['question tag']=q[5]
                    post['no of answers']=len(answer_data)
                    post['question answers']=list(total_answers)
                    total_post.append(post.copy())
                    print('\n\n---')
                    #test(total_post)
                    print('---\n\n')
            return (total_post)
        else:
            print('else part no serach key found')
            for q in question_data:
                #print(q)
                total_answers.clear()
                answer_data=collect_data_form_answers(q[0])
                print('----')
                if len(answer_data)!=0:
                    for a in answer_data:
                        print('\n')
                        answers['answer_id']=a[0]
                        answers['answered by']=a[1]
                        answers['answer timestamp']=a[2]
                        answers['answer']=a[3]
                        answers['answer edit_status']=check_edit_status(session_id,a[4])
                        total_answers.append(answers.copy())
                post['question answer scroll status']=check_scroll_status(len(answer_data))
                post['question answer scroll height']=check_scroll_height(len(answer_data))
                post['question edit_status']=check_edit_status(session_id,q[6])
                post['question_id']=q[0]
                post['question postedby']=q[1]
                post['question timestamp']=q[2]
                post['question title']=q[3]
                post['question description']=q[4]
                post['question tag']=q[5]
                post['no of answers']=len(answer_data)
                post['question answers']=list(total_answers)
                total_post.append(post.copy())
                print('\n\n---')
                #test(total_post)
                print('---\n\n')
            return (total_post)

def gather_data(session_user,select_key='none',search_key ='none'):
    check_scroll_height=lambda x : '0' if x==0 else '140'
    check_scroll_status=lambda x : 'hidden' if x==0 else 'scroll'
    check_edit_status=lambda x,y : 'inline-block' if x==y else 'none'
    post={'question_id':'','question postedby':'','question edit_status':'','question answer scroll status':'','question answer scroll height':'','question timestamp':'','question title':'','question description':'','question tag':'','no of answers':'','question answers':''}
    answers={'answer_id':'','answer edit_status':'','answered by':'','answer timestamp':'','answer':''}
    total_answers=[]
    total_post=[]
    quesion_data=collect_data_from_question(select_key)
    for q in quesion_data:
        total_answers.clear()
        if search_key !='none':
            print("found")
        else:
            answer_data=collect_data_form_answers(q[0])
            if len(answer_data)!=0:
                for a in answer_data:
                    answers['answer_id']=a[0]
                    answers['answered by']=a[1]
                    answers['answer timestamp']=a[2]
                    answers['answer']=a[3]
                    answers['answer edit_status']=check_edit_status(session_user,a[4])
                    total_answers.append(answers.copy())
        post['question answer scroll status']=check_scroll_status(len(answer_data))
        post['question answer scroll height']=check_scroll_height(len(answer_data))
        post['question edit_status']=check_edit_status(session_user,q[6])
        post['question_id']=q[0]
        post['question postedby']=q[1]
        post['question timestamp']=q[2]
        post['question title']=q[3]
        post['question description']=q[4]
        post['question tag']=q[5]
        post['no of answers']=len(answer_data)
        post['question answers']=list(total_answers)
        total_post.append(post.copy())
    return (total_post)

def get_count(table_name,user_id):
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    if table_name =='questions':
        try:
            con = mydb.execute('select count(*) from questions where user_id = ?;',[user_id])
            result1= con.fetchall()
            return (result1)
        except sqlite3.Error as error:
            print(error)
            return (error) 
    elif table_name == 'answers':
        try:
            con = mydb.execute('select count(*) from answers where user_id = ?;',[user_id])
            result1= con.fetchall()
            return (result1)
        except sqlite3.Error as error:
            print(error)
            return (error)


@app.route('/',methods=['post','get'])
def index():
    print('loding home.html')
    if 'userid' in session and 'username' in session:
        useridv = session['userid']
        usernamev = session['username']
        result1 = gather_data1(session_id=useridv)
        print('session data found : ','userid = ',useridv,' username = ', usernamev )
        stat1data='Welcome, '+usernamev+'.'
        stat2data='Total question posted: '+str(get_count('questions',useridv)[0][0]) +' and Total answers replyed: '+str(get_count('answers',useridv)[0][0])+'.'
        return render_template('home.html',userid=useridv,username= usernamev,posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="inline",noPostCondn="none")
    else:
        result1 = gather_data1(session_id=0)
        print('inside session not found')
        app.secret_key = secretkeygeneration()
        stat1data='Welcome, Guest.'
        stat2data='Signin/signup to create post or reply to post'
        return render_template('home.html',userid=0,username='none',posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="none",noPostCondn="inline-block")

@app.route('/signin', methods=['post'])
def sign_in_process_function():
    print('processing sign in request')
    mydb = sqlite3.connect('server_data.db')
    usernameoremail = request.form['name']
    password =request.form['email']
    '''
    print(usernameoremail)
    print(password)
    '''
    try:
        con1 = mydb.execute("SELECT user_id,username FROM authentication WHERE email = ? AND password =?;",[usernameoremail,password])
        result1= con1.fetchall()
        if len(result1)==0:
            print('record not found in database for the requested :','email =',usernameoremail, 'password =',password)
            con2 = mydb.execute("SELECT user_id,username FROM authentication WHERE username = ? AND password =?;",[usernameoremail,password])
            result2= con2.fetchall()
            if len(result2)==0:
                print('record not found in database for the requested :','username =',usernameoremail, 'password =',password)
                print('no record found in the database ')
                return jsonify({'error' : 'username and password are not regonized'})
            else:
                print('record found in database for the requested :','username =',usernameoremail, 'password =',password)
                print('information retrived form the database : ', 'userid =',result2[0][0], 'username = ',result2[0][1])
                session['userid']= result2[0][0]
                session['userid']= result2[0][0]
                session['username']=result2[0][1]
                #return redirect(url_for('index'))
                return jsonify({'ack' : 'signin sucessfull'})
        else:
            print('record found in database for the requested :','email =',usernameoremail, 'password =',password)
            print('information retrived form the database : ', 'userid =',result1[0][0], 'username = ',result1[0][1])
            session['userid']= result1[0][0]
            session['username']=result1[0][1]
            #return redirect(url_for('index'))
            return jsonify({'ack' : 'signin sucessfull'})
    except sqlite3.Error as error:
        print('unexpected error has occured : ',error)
        return jsonify({'error' : 'server is expressing a unexpected error  '+ error})

@app.route('/signup', methods=['post'])
def sign_up_process_function():
    print('processing signup request')
    mydb = sqlite3.connect('server_data.db')
    username=request.form['name']
    useremail=request.form['email']
    userpass1=request.form['pass1']
    userpass2=request.form['pass2']
    '''
    print(username)
    print(useremail)
    print(userpass1)
    print(userpass2)
    '''
    if userpass1 == userpass2:
        try:
            mydb.execute("INSERT INTO authentication (username,email,password)VALUES (?,?,?);",[username,useremail,userpass1]);
            mydb.commit()
            mydb.close()
            mydb = sqlite3.connect('server_data.db')
            con2 = mydb.execute("SELECT user_id,username FROM authentication WHERE username = ? AND password =?;",[username,userpass1])
            result2= con2.fetchall()
            session['userid']= result2[0][0]
            session['username']=result2[0][1]
            #return redirect(url_for('index'))
            return jsonify({'ack' : 'signup sucessfull'})
            print('entry sucessfull')
        except sqlite3.Error as error:
            if error.args[0].find('UNIQUE')==-1:
                print('unexpected error has occured : ',error)
                return jsonify({'error' : 'server is expressing a unexpected error  '+ error})
            else:
                res = error.args[0].partition('.')[2]
                print('integrity error of unique data entry has occured :', res)
                return jsonify({'error' : 'try a different '+res})
    else:
        return jsonify({'error' :'password doesnot match'})

@app.route('/logout',methods=['post'])
def logout():
   print('processing logout request')
   session.pop('userid', None)
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/myposts',methods=['post','get'])
def myposts():
    print('porocessing user post request')
    try:       
        useridv = session['userid']
        usernamev = session['username']
        result1 = gather_data(useridv,useridv)
        stat1data='Welcome, '+usernamev+'. All your post are here'
        stat2data='Total question posted: '+str(get_count('questions',useridv)[0][0]) +' and Total answers replyed: '+str(get_count('answers',useridv)[0][0])+'.'
        return render_template('home.html',userid=useridv,username= usernamev,posts=result1,inPostPage=1,stat1=stat1data,stat2=stat2data,postAnsCondn="inline",noPostCondn="none")
    except:
        return redirect(url_for('index'))

@app.route('/createpost',methods=['post'])
def createpost():
    post_title=request.form['title']
    post_description=request.form['description']
    post_tag=request.form['tag']
    user_id = session['userid']
    index = request.form['location']
    write_post(post_title,post_description,post_tag,user_id)
    return redirect(url_for(location[int(index)]))

@app.route('/updatepost',methods=['post'])
def updatepost():
    post_title=request.form['title']
    post_description=request.form['description']
    post_tag=request.form['tag']
    user_id = session['userid']
    question_id = request.form['quesid']
    index = request.form['location']
    update_post(post_title,post_description,post_tag,question_id,user_id)
    return redirect(url_for(location[int(index)]))

@app.route('/deletepost',methods=['post'])
def deletepost():
    question_id=request.form['qid']
    user_id = session['userid']
    location = request.form['location']
    delete_post(question_id,user_id)
    return redirect(location)
   
@app.route('/createanswer',methods=['post'])
def createanswer():
    print(request.base_url)
    answer=request.form['answer']
    question_id = request.form['qid']
    if 'userid' in session and 'username' in session:
        user_id = session['userid']
        write_answer(answer,user_id,question_id)
        index = request.form['location']
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/deleteans',methods=['post'])
def deleteans():
    print(request.base_url)
    answer_id=request.form['ansid']
    question_id = request.form['qid']
    user_id = session['userid']
    location = request.form['location']
    delete_answer(answer_id,user_id,question_id)
    return redirect(location)

@app.route('/updateans',methods=['post'])
def updateans():
    answer=request.form['answer']
    answer_id = request.form['answerid']
    question_id = request.form['qid']
    user_id = session['userid']
    index = request.form['location']
    update_answer(answer,answer_id,user_id,question_id)
    return redirect(url_for(location[int(index)]))


@app.route('/search',methods=['post','get'])
def search():
   if request.method == 'POST':
       search_key = request.form['search']
       if 'userid' in session and 'username' in session:
            useridv = session['userid']
            usernamev = session['username']
            result1 = gather_data1(session_id=useridv,search_key=search_key)
            stat1data='search result for : '+search_key
            stat2data='Welcome, '+usernamev+'.'
            if not result1:
                return redirect(url_for('index'))
            return render_template('home.html',userid=useridv,username= usernamev,posts=result1,inPostPage=2,stat1=stat1data,stat2=stat2data,postAnsCondn="inline",noPostCondn="none")
       else:
            result1 = gather_data1(session_id=0,search_key=search_key)
            stat1data='search result for : '+search_key
            stat2data='Welcome, Guest.'
            if not result1:
                return redirect(url_for('index'))
            return render_template('home.html',userid=0,username='none',posts=result1,inPostPage=2,stat1=stat1data,stat2=stat2data,postAnsCondn="none",noPostCondn="inline-block")
   
@app.route('/tag',methods=['post','get'])
def tag():
    searchtag = request.args.get('search')
    if 'userid' in session and 'username' in session:
        useridv = session['userid']
        usernamev = session['username']
        print(searchtag)
        result1 = gather_data1(session_id=useridv,select_key_location='tag_id',select_key=searchtag)
        print("username")
        print(result1)
        stat1data='search result for tag : '+searchtag
        stat2data='Welcome, '+usernamev+'.'
        return render_template('home.html',userid=useridv,username= usernamev,posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="inline",noPostCondn="none")
    else:
        result1 = gather_data1(session_id=0,select_key_location='tag_id',select_key=searchtag)
        print(result1)
        stat1data='search result for tag : '+searchtag
        stat2data='Welcome, Guest.'
        return render_template('home.html',userid=0,username='none',posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="none",noPostCondn="inline-block")

@app.route('/tag1',methods=['post','get'])
def tag1():
    searchtag = request.args.get('search')
    import sqlite3
    mydb = sqlite3.connect('server_data.db')
    con=mydb.execute('Select user_id from authentication where username =?;',[searchtag])
    result=con.fetchall()
    print(result)
    print(result[0][0])
    if 'userid' in session and 'username' in session:
        useridv = session['userid']
        usernamev = session['username']
        print(searchtag)
        stat1data='search result for username : '+searchtag
        stat2data='Welcome, '+usernamev+'.'
        result1 = gather_data1(session_id= useridv,select_key_location='user_id',select_key=result[0][0])
        print("username")
        print(result1)
        return render_template('home.html',userid=useridv,username= usernamev,posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="inline",noPostCondn="none")
    else:
        result1 = gather_data1(session_id=0,select_key_location='user_id',select_key=result[0][0])
        print(result1)
        stat1data='search result for username : '+searchtag
        stat2data='Welcome, Guest.'      
        return render_template('home.html',userid=0,username='none',posts=result1,inPostPage=0,stat1=stat1data,stat2=stat2data,postAnsCondn="none",noPostCondn="inline-block")
    
if __name__ == '__main__':
	app.run()