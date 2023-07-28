import os, psycopg2, string, random, hashlib,datetime

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits

    user_id = ''.join(random.choices(charset, k=30))
    return user_id

def get_hash(password, salt):
    b_pw = bytes(password, encoding='utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def make_id():
    charset = string.ascii_letters + string.digits
    userid = ''.join(random.choices(charset, k=15))
    userid = '@' + userid
    return userid

def insert_user(user_id, user_name, birthday, filename, mail, salt, password):
    sql = 'INSERT INTO snsaccount2 VALUES(default, %s, %s, %s, %s, %s, %s, %s)'

    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_id, user_name, birthday, filename, mail, salt, hashed_password))
        count = cursor.rowcount # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError :
        count = 0

    finally :
        cursor.close()
        connection.close()

    return count

def select_all_posts():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM snspost2'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def select_my_posts(mail):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM snspost2 WHERE mail = %s'

    cursor.execute(sql, (mail,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows
def select_account(search):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM snsaccount2  WHERE userid LIKE %s or name LIKE %s'

    pattern=f"%{search}%"

    cursor.execute(sql, (pattern,pattern,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def select_my(mail):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM snsaccount2 WHERE mail = %s'

    cursor.execute(sql, (mail,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()
    return row

def select_name(mail):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT name FROM snsaccount2 WHERE mail = %s'

    cursor.execute(sql, (mail,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()
    return row

def select_filename(mail):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT filename FROM snsaccount2 WHERE mail = %s'

    cursor.execute(sql, (mail,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()
    return row

def insert_post(mail,name,body,filename):
    date = datetime.date.today()

    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO snspost2 VALUES(default, %s, %s, %s, %s, %s)'

    cursor.execute(sql, (mail,name,body,filename,date))
    count = cursor.rowcount # 更新件数を取得
    connection.commit()
    print(count)

    cursor.close()
    connection.close()

def login(mail, password):
    sql = 'SELECT salt, password FROM snsaccount2 WHERE mail = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (mail,))
        user = cursor.fetchone()

        print(user)
        if user != None:
            # SQLの結果からソルトを取得
            salt = user[0]

            # DBから取得したソルト + 入力したパスワード からハッシュ値を取得
            hashed_password = get_hash(password, salt)
            print(hashed_password)
            
            # 生成したハッシュ値とDBから取得したハッシュ値を比較する
            if hashed_password == user[1]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg