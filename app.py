import io
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from dotenv import load_dotenv
import db, string, random, boto3

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['POST'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')

    # ログイン判定
    if db.login(mail, password):
        session['user'] = True      # session にキー：'user', バリュー:True を追加
        session['mail'] = mail
        session.permanent = True    # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=30)   # session の有効期限を 30 分に設定
        return redirect(url_for('top'))
    else :
        error = 'ユーザ名またはパスワードが違います。'
        input_data = {'mail':mail, 'password':password}
        return render_template('index.html', error=error, data=input_data)

@app.route('/top', methods=['GET'])
def top():
    # session にキー：'user' があるか判定
    if 'user' in session:
        post_list = db.select_all_posts()
        return render_template('post/top.html', post_list=post_list)   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト

@app.route('/mypage', methods=['GET'])
def mypage():
    # session にキー：'user' があるか判定
    if 'user' in session:
        mail = session.get('mail')
        my = db.select_my(mail)
        print(my)
        my_post = db.select_my_posts(mail)
        return render_template('post/mypage.html', post_list=my_post, my=my)   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト

@app.route('/register_post')
def register_post():
    if 'user' in session:
        return render_template('post/register_post.html')   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト
@app.route('/post_comp', methods=['POST'])
def post_comp():
    if 'user' in session:
        mail = session.get('mail')
        name = db.select_name(mail)
        body = request.form.get('body')
        print(body)
        filename = db.select_filename(mail)
        db.insert_post(mail,name,body,filename)
        return render_template('post/post_comp.html')   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト
    
@app.route('/setting')
def setting():
    if 'user' in session:
        return render_template('post/setting.html')   # session があれば mypage.html を表示
    else :
        return redirect(url_for('index'))   # session がなければログイン画面にリダイレクト
    
@app.route('/logout')
def logout():
    session.pop('user', None)   # session の破棄
    return redirect(url_for('index'))   # ログイン画面にリダイレクト

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/confirmation', methods=['POST'])
def confirmation():
    user_id = db.make_id()
    user_name = request.form.get('name')
    birthday = request.form.get('birthday')
    uploaded_file = request.files['img']
    file = io.BufferedReader(uploaded_file).read()
    mail = request.form.get('mail')
    filename = mail
    salt = db.get_salt()
    password = request.form.get('password')

    load_dotenv()
    s3 = boto3.client('s3', 'ap-northeast-1')
    s3_bucket = 'profile-image-4221104'
    filename = uploaded_file.filename
    response = s3.put_object(
        Body = file,
        Bucket = s3_bucket,
        Key = filename
    )

    session['user_id'] = user_id
    session['user_name'] = user_name
    session['birthday'] = birthday, 
    session['filename'] = filename
    session['mail'] = mail 
    session['salt'] = salt
    session['password'] = password

    return render_template('confirmation.html', user_id=user_id, user_name=user_name, birthday=birthday, filename=filename, mail=mail,  salt=salt, password=password)

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    birthday = session.get('birthday')
    filename = session.get('filename')
    mail = session.get('mail')
    salt = session.get('salt')
    password = session.get('password')
    
    print(user_name)
    count = db.insert_user(user_id, user_name, birthday, filename, mail, salt, password)


    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)