import pymysql
import datetime
from requests import get
import shutil
import datetime
import requests
import pickle

user_info = {}
# http://hancomtasking.com/upload_data/20220103_mapfile_parser.zip


def download():
    version_from_db = get_version_from_db()
    download_filename = version_from_db + '_mapfile_parser.zip'
    # download_filename = db_version + '_mapfile_parser.zip'
    url = "http://hancomtasking.com/upload_data/" + download_filename
    # print(f'[02/03] url : {url}')
    # with requests.get(url, stream=True) as r:
    #     with open(download_filename, "wb") as f:
    #         shutil.copyfileobj(r.raw, f)
    r = requests.get(url, stream=True, verify=False)
    with open(download_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return True


def version_check(cur_version):
    cur_version_date = datetime.datetime.strptime(cur_version, '%Y%m%d')

    # print(f'[12/25] current version : {cur_version_date}')
    version_from_db = get_version_from_db()
    db_version_date = datetime.datetime.strptime(version_from_db, '%Y%m%d')
    # print(f'[12/25] db_version_date : {db_version_date}')

    if db_version_date > cur_version_date:
        return True
    else:
        return False



def get_version_from_db():
    conn, cursor = db_connect()
    sql = "select * from ver_tbl"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)

    db_version = ''
    for row in records:
        db_version = row[1]

    # print(f'[02/03] db_version : {db_version}')
    return db_version


def db_connect():
    conn = pymysql.connect(host='db.hancomtasking.com',
                           user='tasking123', password='tasking123', db='dbtasking123', charset='utf8')
    cursor = conn.cursor()

    return conn, cursor


def db_execute_quiry(cursor, sql):
    # sql = "SELECT * FROM dummy_gps"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def db_close(conn):
    conn.commit()
    conn.close()


def check_account(user_id, passwd):
    conn, cursor = db_connect()
    sql = "select * from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    if len(records) == 0:
        return False

    for row in records:
        db_user_id = row[1]
        db_passwd = row[2]
        db_activate = row[12]
    # if db_user_id == user_id and db_passwd == passwd and db_activate == '1':
    if db_user_id == user_id and db_passwd == passwd:
        return True
    else:
        return False


def check_activate(user_id):
    conn, cursor = db_connect()
    sql = "select activate,issue_date from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    if len(records) == 0:
        return 0

    for row in records:
        db_activate = row[0]
        str_db_issue_date = row[1]

        if db_activate == '1':  # 활성 mode
            return 1
        elif db_activate == '2':  # demo mode
            return 2
        else:                   # 비활성 mode
            return 0


def check_demo_status(user_id):
    conn, cursor = db_connect()
    sql = "select activate,issue_date from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    if len(records) == 0:
        return False

    for row in records:
        db_activate = row[0]
        str_db_issue_date = row[1]
        str_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        current_date = datetime.datetime.strptime(
            str_current_date, '%Y-%m-%d')
        db_one_month_after_issue_date = datetime.datetime.strptime(
            str_db_issue_date.rstrip(), '%Y-%m-%d')
        db_one_month_after_issue_date = db_one_month_after_issue_date + \
            datetime.timedelta(days=30)

        if current_date > db_one_month_after_issue_date:
            return False
        else:
            return True


def get_demo_date(user_id):
    conn, cursor = db_connect()
    sql = "select issue_date from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    str_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    current_date = datetime.datetime.strptime(str_current_date, '%Y-%m-%d')
    # print(f'[12/13] current_date : {current_date}')
    for row in records:
        str_db_issue_date = row[0]
        # print(f'str_db_expired_date :{str_db_expired_date}')
        db_issue_date = datetime.datetime.strptime(
            str_db_issue_date.rstrip(), '%Y-%m-%d')
        db_one_month_after_issue_date = db_issue_date + \
            datetime.timedelta(days=30)
        # print(f'[12/13] current_date : {current_date}')
        break

    str_db_one_month_after_issue_date = db_one_month_after_issue_date.strftime(
        '%Y-%m-%d')
    diff_days = db_one_month_after_issue_date - current_date

    return str_db_one_month_after_issue_date, str(diff_days.days)


def get_expired_date(user_id):
    conn, cursor = db_connect()
    sql = "select expired_date from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    str_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    current_date = datetime.datetime.strptime(str_current_date, '%Y-%m-%d')
    # print(f'[12/13] current_date : {current_date}')
    for row in records:
        str_db_expired_date = row[0]
        # print(f'str_db_expired_date :{str_db_expired_date}')
        db_expired_date = datetime.datetime.strptime(
            str_db_expired_date.rstrip(), '%Y-%m-%d')
        # print(f'[12/13] current_date : {current_date}')
        break

    diff_days = db_expired_date - current_date
    return str_db_expired_date, str(diff_days.days)


def check_expired_date(user_id):
    conn, cursor = db_connect()
    sql = "select expired_date from members where email = %s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    if len(records) == 0:
        return False

    str_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    current_date = datetime.datetime.strptime(str_current_date, '%Y-%m-%d')
    # print(f'[12/13] current_date : {current_date}')
    for row in records:
        str_db_expired_date = row[0]
        # print(f'str_db_expired_date :{str_db_expired_date}')
        db_expired_date = datetime.datetime.strptime(
            str_db_expired_date.rstrip(), '%Y-%m-%d')
        # print(f'[12/13] current_date : {current_date}')
        if current_date <= db_expired_date:
            return True
        else:
            # update_activate_by_expired_date(user_id)
            return False


def update_deactivate_by_expired_date(user_id):
    conn, cursor = db_connect()
    sql = "update members set activate = '0' where email= %s"
    cursor.execute(sql, (user_id))
    conn.commit()

    db_close(conn)


def update_activate_by_expired_date(user_id):
    conn, cursor = db_connect()
    sql = "update members set activate = '1' where email= %s"
    cursor.execute(sql, (user_id))
    conn.commit()

    db_close(conn)


def get_news():
    news_list = []

    conn, cursor = db_connect()
    sql = "select * from edu"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)

    for row in records:
        news_list.append([row[1], row[2]])

    return news_list


def check_duplicate_account(email_id):
    conn, cursor = db_connect()
    sql = "select * from members where email = %s"
    cursor.execute(sql, (email_id))

    records = cursor.fetchall()
    db_close(conn)

    if records:
        return False
    else:
        return True


def get_company_name():
    company_name_list = []
    conn, cursor = db_connect()
    sql = "select * from company_name order by name"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)

    for row in records:
        company_name_list.append(row[1])

    return company_name_list


def get_user_info(user_id):
    user_profile = {}
    conn, cursor = db_connect()
    sql = "select * from members where email=%s"
    cursor.execute(sql, (user_id))

    records = cursor.fetchall()
    db_close(conn)

    for row in records:
        user_profile = {"email": row[1], "pass": row[2], "contact": row[3], "serial_no": row[4],
                        "licence_type": row[5], "company_name": row[6], "tema_name": row[7]}
        break

    return user_profile


def get_execution_counter(user_id):
    exec_counter = 0
    conn, cursor = db_connect()
    sql = "select * from members where email=%s"
    cursor.execute(sql, (user_id))
    records = cursor.fetchall()
    db_close(conn)

    for row in records:
        exec_counter = row[11]
        break

    return exec_counter


def update_latest_login_date(user_id, lastest_login_date):
    conn, cursor = db_connect()
    sql = "update members set last_login_date = %s where email=%s"
    cursor.execute(sql, (lastest_login_date, user_id))
    conn.commit()

    db_close(conn)


def update_execution_counter(user_id, execution_counter):
    # print(f'update exec_counter => {user_id},{execution_counter}')
    conn, cursor = db_connect()
    sql = "update members set executions_counter = %s where email=%s"
    cursor.execute(sql, (execution_counter, user_id))
    conn.commit()

    db_close(conn)


# def update_demo_date_test(user_id):
#     str_current_date = datetime.datetime.today().strftime('%Y-%m-%d')
#     current_date = datetime.datetime.strptime(
#         str_current_date, '%Y-%m-%d')
#     issue_date_test = current_date - datetime.timedelta(days=30)
#     str_issue_date_test = issue_date_test.strftime('%Y-%m-%d')
#     str_issue_date_test = '2022-01-01'
#     print(f'str_issue_date_test: {str_issue_date_test}')

#     conn, cursor = db_connect()
#     sql = "update members set issue_date = %s where email= %s"
#     cursor.execute(sql, (str_issue_date_test, user_id))
#     conn.commit()
  

def insert_log_data(user_id, lastest_login_date):
    exec_counter = 0
    conn, cursor = db_connect()
    sql = "select company_name, serial_no, issue_date, expired_date, contact, name from members where email=%s"
    cursor.execute(sql, (user_id))
    records = cursor.fetchall()
    db_close(conn)

    company_name = ''
    for row in records:
        company_name = row[0]
        serial_no = row[1]
        issue_date = row[2]
        expired_date = row[3]
        contact = row[4]
        user_name = row[5]
        break

    if company_name != '':
        conn, cursor = db_connect()
        sql = "INSERT INTO logs (email, contact, serial_no,  company_name, issue_date, expired_date, login_date, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, contact, serial_no,
                       company_name, issue_date, expired_date, lastest_login_date, user_name))
        conn.commit()
        db_close(conn)

        return True
    else:
        return False


def insert_user_account(user_name, user_email, passwd, contact_info, serial_no_info, licence_type_info, company_name_info, team_name):
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')

    expired_date = datetime.datetime.today() + datetime.timedelta(days=14)
    # print(f'[12/31] type(expired_date) : {type(expired_date)}')
    generated_expired_date = expired_date.strftime('%Y-%m-%d')
    conn, cursor = db_connect()
    sql = "INSERT INTO members (name, email, pass, contact, serial_no, licence_type, company_name, team_name, issue_date, expired_date,last_login_date, register_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_name, user_email, passwd, contact_info,
                   serial_no_info, licence_type_info, company_name_info, team_name, current_date, generated_expired_date, current_date, current_date))
    db_close(conn)

    conn, cursor = db_connect()
    status = check_account(user_email, passwd)
    db_close(conn)

    profile = get_user_info(user_email)
    profile_file = open('profile.pkl', 'wb')
    profile_user_name = profile["email"]
    # print(f'[12/31] Saved profile_user_name : {profile_user_name}')
    pickle.dump(profile, profile_file)
    profile_file.close()

    if status:
        return True
    else:
        return False


def get_subjects_list_db():
    conn, cursor = db_connect()
    sql = "select * from Subject"
    cursor.execute(sql)
    subjects_list = []
    subject_dict = {}
    records = cursor.fetchall()
    db_close(conn)
    for row in records:
        subject_dict["subject_id"] = row[1]
        subject_dict["subject_name"] = row[2]
        subject_dict["category"] = row[3]
        subjects_list.append(subject_dict)

    if len(records) > 0:
        return True, subjects_list  # extracted_student_json
    else:
        return False  # None


def check_user_email_from_db(u_email):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True  # extracted_student_json
    else:
        return False  # None


def get_all_user_info_from_db():
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            email = row[1]
            user_info[email] = row[2]
        return user_info
    else:
        user_info['ryan@gmail.com'] = '123456'
        return user_info


def get_user_info_from_db(u_email):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_email))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:

            is_student = row[3]
            is_solver = row[4]
            user_school_name = row[6]
            user_school_code = row[7]
            user_grade = row[5]
            if is_student == '1' and is_solver == '1':
                role = 'both'
            elif is_student == '1' and is_solver == '0':
                role = 'student'
            elif is_student == '0' and is_solver == '1':
                role = 'solver'
            else:
                role = 'nothing'
            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)

        return True  # extracted_student_json
    else:
        return False  # None


def insert_user_db(u_id, u_passwd):  # OK
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "INSERT INTO User (userEmail, userPass, userRole, userGrade, schoolName, schoolCode) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (u_id, u_passwd, '0', '10',
                   'Texas Highschool', '0001'))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (u_id, u_passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def update_user_info_db(email, passwd, role, school_name, school_code, grade):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    sql = "update User SET userRole = %s , SchoolName = %s , SchoolCode = %s , userGrade = %s where userEmail = %s and userPass = %s"

    cursor.execute(sql, (role, school_name, school_code, grade, email, passwd))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from User where userEmail = %s and userPass = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def get_user_info_db(email, passwd):
    role = school_name = school_code = grade = ''
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s and userPass = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (email, passwd))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            role = row[3]
            school_name = row[5]
            school_code = row[6]
            grade = row[4]

            # student_data = {"role" : role, "schoolName": user_school_name, "schoolCode" : user_school_code, "grade" : user_grade}
            # extracted_student_json = json.dumps(student_data)

    return role, school_name, school_code, grade


def check_password(u_id, u_passwd):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where userEmail = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (u_id))

    records = cursor.fetchall()
    for row in records:
        print(f'user id : {row[1]}')
        print(f'user passwd : {row[2]}')
    db_close(conn)

    if u_id == row[1] and bcrypt.check_password_hash(row[2], u_passwd):
        return True
    else:
        return False


def check_school_code(school_code):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where schoolCode = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_code))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def check_school_name(school_name):
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from User where schoolCode = %s"
    # sql = "select * from dummy_gps2 where id = %s and timestep = %s"
    cursor.execute(sql, (school_name))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        return True
    else:
        return False


def get_user_question_db(email, subject_id, page):
    question_list = list()
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question where author_email = %s ORDER by question_id DESC"
    cursor.execute(sql, (email))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            # row[4] : subject_name, row[6] : content
            question_list.append(row[4])
        return True, question_list
    else:
        return False, question_list


def get_question_list_all_db(query_str):
    query_str = list()
    question_list = {'question': query_str}

    if len(query_str) == 0:
        conn, cursor = db_connect()
        # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
        sql = "select * from Question ORDER by question_id DESC"
        cursor.execute(sql)

        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:

            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[2]
                subject_name = row[3]
                category = row[4]
                content = row[5]
                created = row[6]
                image_url = row[7]
                recognized_text = row[8]

                # row[4] : subject_name, row[6] : content
                query_str.append(content)
            question_list['question'] = query_str
            return True, question_list
        else:
            return False, question_list
    else:
        return False, question_list


def query_empty_subject_id_empty_db(query, email, subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_empty_db ]')
    print(f'page : {page}')
    print(f'num : {num}')
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # if (int(page) > 0):
    #     sql = "select * from Question order by question_id DESC LIMIT 10 "
    #     cursor.execute(sql)
    # else:
    if len(email) == 0:
        if len(num) == 0:
            sql = "select * from Question order by question_id DESC"
            cursor.execute(sql)
        else:
            sql = "select * from Question order by question_id DESC LIMIT "+num
            cursor.execute(sql)
    else:
        if len(num) == 0:
            sql = "select * from Question where author_email = '" + \
                email + "' order by question_id DESC"
        else:
            sql = "select * from Question where author_email = '" + \
                email + "' order by question_id DESC LIMIT "+num
        print(f'sql : {sql}')
        cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        # query_str_data = []
        # query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, has_correct_answer]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)

    return question_list


def query_empty_subject_id_NOT_empty_db(query, email, subject_id, page, num, hasAnswer):
    question_list = []
    print('[ query_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # if (int(page) > 0):
    #     sql = "select * from Question where subject_id = %s order by question_id DESC LIMIT 10 "
    #     cursor.execute(sql, (subject_id))
    # else:

    if len(email) == 0:
        if len(num) == 0:
            sql = "select * from Question where subject_id = %s order by question_id DESC"
        else:
            sql = "select * from Question where subject_id = %s order by question_id DESC LIMIT " + num
    else:
        if len(num) == 0:
            sql = "select * from Question where subject_id = %s and author_email = '" + \
                email + "' order by question_id DESC"

        else:
            sql = "select * from Question where subject_id = %s and author_email = '" + \
                email + "' order by question_id DESC LIMIT " + num
    print(f'sql : {sql}')
    cursor.execute(sql, (subject_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        # query_str_data = []
        # query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, has_correct_answer]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            # print(f'str : {str}')
            question_list.append(str)
    return question_list


def converted_special_char(data):
    str = data

    str = str.replace('\n', '')
    # str = str.strip('\\')
    str = str.replace('\\', '')
    str = str.replace('\\', '')
    # regex = re.compile((r'\\'))
    # conv_txt = regex.sub("\\", "", str)
    text = re.sub(
        '<>#/\:$.@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》', '', str)

    # print(f'text : {text}')
    text = text.replace('<latex>', '')
    text = text.replace('</latex>', '')
    return text


def query_NOT_empty_subject_id_empty_db(origin_query, email, subject_id, page, num, hasAnswer):
    selected_question_id = -1
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_empty_db ]')
    print('len of query > 0')
    print(f'subject_id : {subject_id}')
    # if leng_of_subject_id == 0:
    conn, cursor = db_connect()

    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    sql_start = "select * from Question "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    print(f'len of records : {len(records) }')
    if len(records) > 0:
        # query_str_data = []
        # query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, has_correct_answer]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)

    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]

            selected_question_id = row[1]
            if len(question_list) == 0:
                selected_question_id = question_id
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]

            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text]

            # row[4] : subject_name, row[6] : content
        answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    if len(question_list) == 0 and len(answer_list) != 0:
        conn, cursor = db_connect()
        sql_start = "select * from Answer where question_id =" + selected_question_id
        cursor.execute(sql)
        db_close(conn)
        print(f'len of records : {len(records) }')
        if len(records) > 0:
            # query_str_data = []
            # query_str_list = []
            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[2]
                subject_name = row[3]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                has_correct_answer = row[10]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, has_correct_answer]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)

    return question_list, answer_list


def query_NOT_empty_subject_id_NOT_empty_db(origin_query, email, subject_id, page, num, hasAnswer):
    question_list = []
    answer_list = []
    print('[ query_NOT_empty_subject_id_NOT_empty_db ]')
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # if (int(page) > 0):
    #     print(f'subject_id : {subject_id}')
    #     sql = "select * from Question where recognized_text LIKE '%" + query + "%' " + \
    #         "and subject_id = '" + subject_id + "'order by question_id DESC LIMIT 10"
    #     print(f'sql : {sql}')
    #     cursor.execute(sql, )
    # else:
    query = converted_special_char(origin_query)
    print(f'conv_query : {query}')
    sql_start = "select * from Question "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "

    option_2 = "OR re_con LIKE '%" + query + "%' "
    option_3 = ") AND subject_id = '" + subject_id + "'"
    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + option_3 + sql_end
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + option_3 + sql_end
        cursor.execute(sql)
    # sql = "select * from Question where recognized_text LIKE '%" + query + "%' " + \
    #     "and subject_id = '" + subject_id + "' order by question_id DESC LIMIT %s"

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        # query_str_data = []
        # query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]
            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, has_correct_answer]
            print(query_str_data)
            # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
            str = make_question_dict_str(query_str_data)
            print(f'str : {str}')
            question_list.append(str)

    conn, cursor = db_connect()

    sql_start = "select * from Answer "
    if len(email) == 0:
        option_1 = "where (re_recog LIKE '%" + query + "%' "
    else:
        option_1 = "where author_email = '" + email + \
            "' and (re_recog LIKE '%" + query + "%' "
    option_2 = "OR re_con LIKE '%" + query + "%') "

    if len(num) == 0:
        sql_end = "order by question_id DESC"
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    else:
        sql_end = "order by question_id DESC LIMIT " + num
        sql = sql_start + option_1 + option_2 + sql_end
        print(f'sql : {sql}')
        cursor.execute(sql)
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    # sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    # cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = row[0]
            question_id = row[1]
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]

            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text]

            # row[4] : subject_name, row[6] : content
        answer_list.append(make_answer_dict_str(answer_str_data))
        # answer_str_list.append(answer_str_data)
        # print(f'answer_str_list : {answer_str_list}')
        # # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        # for answer_data in answer_str_list:
        #     answer_list.append(make_answer_dict_str(answer_data))

    return question_list, answer_list


def get_question_ids_list_db(question_ids, number_question_ids):
    print('[ get_question_ids_list_db ]')
    query_str = list()
    question_list = []

    print(f'question_ids : {question_ids}')
    print(f'number_question_ids : {number_question_ids}')

    if number_question_ids == 0:
        sql = "select * from Question order by question_id DESC"
        conn, cursor = db_connect()
        cursor.execute(sql)
        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            # query_str_data = []
            # query_str_list = []
            for row in records:
                question_id = row[0]
                author_email = row[1]
                subject_id = row[2]
                subject_name = row[3]
                category = row[4]
                content = row[5]
                created = row[6]
                updated = row[7]
                image_url = row[8]
                recognized_text = row[9]
                has_correct_answer = row[10]
                query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                  content, created, updated, image_url, recognized_text, has_correct_answer]
                print(query_str_data)
                # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                str = make_question_dict_str(query_str_data)
                print(f'str : {str}')
                question_list.append(str)
        return True, question_list
    else:
        for ids in question_ids:
            # ids = question_ids[0]
            sql_start = "select * from Question"
            sql_content = ' where '
            sql_content = sql_content + "question_id = " + ids
            sql_end = " order by question_id DESC"
            sql = sql_start + sql_content + sql_end
            print(f'sql : {sql}')
            conn, cursor = db_connect()
            cursor.execute(sql)
            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                # query_str_data = []
                # query_str_list = []
                for row in records:
                    question_id = row[0]
                    author_email = row[1]
                    subject_id = row[2]
                    subject_name = row[3]
                    category = row[4]
                    content = row[5]
                    created = row[6]
                    updated = row[7]
                    image_url = row[8]
                    recognized_text = row[9]
                    has_correct_answer = row[10]
                    query_str_data = [question_id, author_email, subject_id, subject_name, category,
                                      content, created, updated, image_url, recognized_text, has_correct_answer]
                    print(query_str_data)
                    # query_str_list.append(query_str_data) # row[4] : subject_name, row[6] : content
                    str = make_question_dict_str(query_str_data)
                    print(f'str : {str}')
                    question_list.append(str)
        return True, question_list


def get_question_list_query_db(query, email, subject_id, page, num, hasAnswer):
    print('[ get_question_list_query_db ]')
    query_str = list()
    question_list = []
    answer_list = []
    print(f'query : {query}')
    print(f'subject_id : {subject_id}')
    print(f'email : {email}')
    print(f'page : {page}')
    print(f'num : {num}')
    print(f'hasAnswer : {hasAnswer}')
    if len(query) == 0:
        if len(subject_id) == 0:
            question_list = query_empty_subject_id_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list = query_empty_subject_id_NOT_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
    else:
        if len(subject_id) == 0:
            question_list, answer_list = query_NOT_empty_subject_id_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            # print(
            # f'[get_question_list_query_db-->question_list] : {question_list}')
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list
        else:
            question_list, answer_list = query_NOT_empty_subject_id_NOT_empty_db(
                query, email, subject_id, page, num, hasAnswer)
            if len(question_list) != 0 or len(answer_list) != 0:
                return True, question_list, answer_list
            else:
                return False, question_list, answer_list


def make_question_dict_str(query):
    # print(f'make_question_dict_str')
    # print(query)
    # print(f'query_str_list size : {len(query_str_list)}')
    # query_dict_list = []

    print(f'query : {query}')
    query_dict = {}
    query_dict["question_id"] = str(query[0])
    query_dict["author_email"] = query[1]
    query_dict["subject_id"] = query[2]
    query_dict["subject_name"] = query[3]
    query_dict["category"] = query[4]
    query_dict["content"] = query[5]
    query_dict["created"] = query[6]
    query_dict["updated"] = query[7]
    query_dict["image_url"] = query[8]
    query_dict["recognized_text"] = query[9]
    query_dict["has_correct_answer"] = query[10]

    # json_query_dict = json.dumps(query_dict)
    # json_query_dict = json_query_dict.strip().replace('\"','"')
    # query_dict_list.append(query_dict)
    # print(query_dict_list)

    # with open('question.json', 'w') as outfile:
    #     json.dump(query_dict_list, outfile, indent=4)

    return query_dict


def make_answer_dict_str(answer):
    print('[ make_answer_dict_str ]')
    # print(answer_str_list)
    # print(f'answer_str_list size : {len(answer_str_list)}')
    # answer_dict_list = []

    # for answer in answer_str_list:
    print(f'answer : {answer}')
    answer_dict = {}
    answer_dict["answer_id"] = answer[0]
    answer_dict["question_id"] = answer[1]
    answer_dict["author_email"] = answer[2]
    answer_dict["content"] = answer[3]
    answer_dict["selected"] = answer[4]
    answer_dict["created"] = answer[5]
    answer_dict["updated"] = answer[6]
    answer_dict["image_url"] = answer[7]
    answer_dict["recognized_text"] = answer[8]
    # json_answer_dict = json.dumps(answer_dict)

    print(f'answer_dict : {answer_dict}')
    return answer_dict


def get_question_list_db(query_str, subject_id, page):
    print('[ get_question_list_db ]')
    answer_list = list()
    answer_list = {'question': query_str}

    question_list = {'search_keywords': query_str, 'answer': answer_list}
    question_id_list = []

    query_str_list = query_str.split(',')

    for i in range(len(query_str_list)):
        query_str_list[i] = query_str_list[i].replace(' ', '')

    print(f'len of query_str : {len(query_str_list)}')
    print(f'query_str : {query_str_list}')
    for search_item in query_str_list:
        conn, cursor = db_connect()
        # search_sql = "select question_id from Question where recognized_text '{0}".format('%')
        # search_sql = search_sql + search_item + "{}'".format('%')get_question_list_query_db
        search_sql = "select question_id from Question where recognized_text '%" + \
            search_item + "%'"
        print(f'sql : {search_sql}')
        cursor.execute(search_sql)
        records = cursor.fetchall()
        db_close(conn)
        if len(records) > 0:
            for row in records:
                question_id_list.append(row[0])

    if len(question_id_list) > 0:
        print(f'question_id_list : {question_id_list}')
        for search_id in question_id_list:
            print(f'question_id_list : {search_id}')
            conn, cursor = db_connect()
            sql = "select * from Answer where question_id = %s ORDER BY answer_id"
            cursor.execute(sql, (str(search_id)))
            records = cursor.fetchall()
            db_close(conn)
            if len(records) > 0:
                for row in records:
                    answer_id = row[0]
                    question_id = row[1]
                    author_emial = row[2]
                    content = row[3]
                    selected = row[4]
                    created = row[5]
                    updated = row[6]
                    image_url = row[7]
                    recognized_text = row[8]
                    # row[4] : subject_name, row[6] : content
                    answer_list.append(content)
                question_list['answer'] = answer_list
                return True, question_list
            else:
                return False, question_list


def get_answer_for_question_db(email, question_id):
    print('[ get_answer_for_question_db ]')
    answer_str = list()
    question_str = list()
    question_list = {}
    answer_list = []
    flag_question_is = False

    print(f'question_id : {question_id}')
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question where question_id = %s ORDER by question_id DESC"
    cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        flag_question_is = True
        query_str_data = []
        query_str_list = []
        for row in records:
            question_id = row[0]
            author_email = row[1]
            subject_id = row[2]
            subject_name = row[3]
            category = row[4]
            content = row[5]
            created = row[6]
            updated = row[7]
            image_url = row[8]
            recognized_text = row[9]
            has_correct_answer = row[10]

            query_str_data = [question_id, author_email, subject_id, subject_name, category,
                              content, created, updated, image_url, recognized_text, has_correct_answer]

            # row[4] : subject_name, row[6] : content
            query_str_list.append(query_str_data)
        question_list = make_question_dict_str(query_str_list[0])
        print(f'question_list : {question_list}')

    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Answer where question_id = %s ORDER BY answer_id"
    cursor.execute(sql, (question_id))

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        answer_str_data = []
        answer_str_list = []
        for row in records:
            answer_id = str(row[0])
            question_id = row[1]
            author_email = row[2]
            content = row[3]
            selected = row[4]
            created = row[5]
            updated = row[6]
            image_url = row[7]
            recognized_text = row[8]

            answer_str_data = [answer_id, question_id, author_email, content,
                               selected, created, updated, image_url, recognized_text]

            # row[4] : subject_name, row[6] : content
            answer_str_list.append(answer_str_data)
        print(f'answer_str_list : {answer_str_list}')
        # answer_list['answer'] = make_answer_dict_str(answer_str_list)
        for answer_data in answer_str_list:
            answer_list.append(make_answer_dict_str(answer_data))

        return True, question_list, answer_list
    else:
        if flag_question_is:
            return True, question_list, answer_list
        else:
            return False, question_list, answer_list


def create_question_db(email, subject_name, subject_id, category, content, imageUrl, recog_text):
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    print(f'email : {email}')
    print(f'subject_name : {subject_name}')
    print(f'subject_id : {subject_id}')
    print(f'category : {category}')
    print(f'content : {content}')
    print(f'created_date : {created_date}')
    print(f'imageUrl : {imageUrl}')
    print(f'recog_text : {recog_text}')
    conn, cursor = db_connect()

    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)
    sql = "INSERT INTO Question (author_email, subject_id, subject_name, category, content,  created, image_Url, recognized_text, has_correct_answer, re_con, re_recog) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (email, subject_id, subject_name,
                   category, content, created_date, imageUrl, recog_text, conv_content, conv_recog_text, str(0)))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Question where author_email = %s and subject_name = %s"
    cursor.execute(sql, (email, subject_name))
    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            q_no = str(row[0])
    else:
        q_no = str(-1)

    return q_no


def create_write_answer_db(email, question_id, content, imageUrl, recog_text):
    current_datetime = datetime.now()
    created_date = str(current_datetime)
    print(f'created_date : {created_date}')
    print(f'imageUrl : {imageUrl}')
    conv_content = converted_special_char(content)
    conv_recog_text = converted_special_char(recog_text)
    conn, cursor = db_connect()
    sql = "INSERT INTO Answer (author_email, question_id, content, created, image_Url, recognized_text, re_con, re_recog) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (email, question_id, content,
                   created_date, imageUrl, recog_text, conv_content, conv_recog_text))
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Answer where author_email = %s and question_id = %s"
    cursor.execute(sql, (email, question_id))
    records = cursor.fetchall()

    db_close(conn)

    if len(records) > 0:
        for row in records:
            ano_no = str(row[0])
    else:
        ano_no = str(-1)

    return ano_no


def delete_write_answer_db(answer_id):

    conn, cursor = db_connect()
    sql = "DELETE FROM Answer WHERE answer_id = " + str(answer_id)
    cursor.execute(sql)
    db_close(conn)

    conn, cursor = db_connect()
    sql = "select * from Answer where answer_id = " + str(answer_id)
    cursor.execute(sql)
    records = cursor.fetchall()
    db_close(conn)

    if len(records) > 0:
        return False
    else:
        return True


def recent_question_db(question_num):
    question_list = list()
    conn, cursor = db_connect()
    # sql = "insert into gps(timestep, id, x,y) values(%s,%s,%s,%s)"
    sql = "select * from Question order by question_id DESC limit 10"
    cursor.execute(sql)

    records = cursor.fetchall()
    db_close(conn)
    if len(records) > 0:
        for row in records:
            question = []
            question.append(row[0])
            question.append(row[1])
            question.append(row[2])
            question.append(row[3])
            question.append(row[4])
            question.append(row[5])
            question.append(row[8])
            question.append(row[9])

            question_list.append(question)
    return question_list
