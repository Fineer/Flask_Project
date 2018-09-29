# -*- coding: utf-8 -*-
import sqlite3

'''
author: Zhang Xiaofan
        Zhou Xi
'''


def buy_info_service(school, user_name):
    # 学校购买信息系统服务，user_name是管理员邮箱
    # 没有密码 权限选择的参数未知
    # 成功返回0 失败返回-1
    # 默认购买了师生信息项目，没有打开课程和分数权限
    con = sqlite3.connect('database\\' + 'admin.db')
    try:
        sql = '''INSERT INTO "admininfo"("mail", "info", "course", "score")''' \
              '''VALUES ('%s', '%s', '%s', '%s');''' % (user_name, 'true', 'false', 'false')
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        # 创建数据库
        con = sqlite3.connect('database\\' + school + '.db')
        try:
            sql = 'CREATE TABLE teacherinfo(tid TEXT KEY NOT NULL, name TEXT NOT NULL,' \
                  'mail TEXT Primary KEY NOT NULL, password TEXT, phone TEXT, privilege Boolean);'
            con.execute(sql)
            sql = 'CREATE TABLE studentinfo(sid TEXT KEY NOT NULL, name TEXT NOT NULL,' \
                  'mail TEXT Primary KEY NOT NULL, password TEXT, phone TEXT, privilege Boolean);'
            con.execute(sql)
            sql = 'CREATE TABLE courseinfo(cid TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL,' \
                  'tid TEXT NOT NULL, time TEXT, classroom TEXT, introduction TEXT);'
            con.execute(sql)
            sql = 'CREATE TABLE scoreinfo(cid TEXT NOT NULL, sid TEXT NOT NULL,' \
                  'score TEXT, level TEXT, key TEXT PRIMARY KEY NOT NULL, cname TEXT);'
            con.execute(sql)
            sql = 'CREATE TABLE seleCourseInfo(cid TEXT NOT NULL, sid TEXT NOT NULL,' \
                  'key TEXT PRIMARY KEY NOT NULL);'
            con.execute(sql)
        except:
            return -1;
        else:
            con.commit()
            con.close()
            return 0


# print(buy_info_service('bbb', 'hhh'))

def buy_score_service(school, user_name):
    # 更改score权限为true
    # 成功返回0 失败返回1
    con = sqlite3.connect('database\\' + 'admin.db')
    try:
        sql = 'UPDATE admininfo SET score = \'%s\' WHERE mail = \'%s\';' % ('true', user_name)
        con.execute(sql)
    except:
        return -1;
    else:
        con.commit()
        con.close()
        return 0


def buy_course_service(school, user_name):
    # 更改course权限为true
    # 成功返回0 失败返回1
    con = sqlite3.connect('database\\' + 'admin.db')
    try:
        sql = 'UPDATE admininfo SET course = \'%s\' WHERE mail = \'%s\';' % ('true', user_name)
        con.execute(sql)
    except:
        return -1;
    else:
        con.commit()
        con.close()
        return 0


def get_services(school):
    # 根据school，返回该校是否购买了info_service, course_service, score_service. （信息系统，选课系统，成绩系统）
    # return 3个 bool 型变量，第一个对应是否购买了info_service，第二个对应course_service， 第三个对应score_service
    # return True, True, True
    con = sqlite3.connect('database\\' + 'admin.db')
    sql = 'SELECT * FROM admininfo WHERE mail LIKE\'%%%s%%\';' % (school)
    cursor = con.execute(sql)
    for row in cursor:
        info = row[2]
        course = row[3]
        score = row[4]
    con.close()
    return info, course, score


def get_days(school):
    con = sqlite3.connect('database\\' + 'admin.db')
    sql = 'SELECT * FROM admininfo WHERE mail LIKE\'%%%s%%\';' % (school)
    cursor = con.execute(sql)
    for row in cursor:
        info_end = row[5]
        course_end = row[6]
        score_end = row[7]
    con.close()
    return info_end, course_end, score_end


def login_match(mail, password):
    # Q: 验证完登陆是否成功用不用返回一个确认信息？我把验证结果都pass了
    # 用 postfix 查询得到学校名，用 mail 和 password 验证是否登录成功。mail.sustc.edu.cn, sustc.edu.cn
    # 最终返回 学校名 和 身份(admin, teacher, student），如果身份都不满足，则用'-1'代替身份
    # 密码错误的话 return school, '-1'

    # 判断身份
    atindex = mail.find('@')
    postfix = mail[atindex + 1: len(mail)]
    postfix_splite = postfix.split(".")
    school = postfix_splite[len(postfix_splite) - 3]
    print(school)
    if (len(postfix_splite) == 4):
        identity = 'student'
    elif (postfix_splite[len(postfix_splite) - 2] == 'edu'):
        identity = 'teacher'
    elif (postfix_splite[len(postfix_splite) - 2] == 'adm'):
        identity = 'admin'
    else:
        identity = '-1'
    print(identity)

    # 管理员登陆验证
    if (identity == 'admin'):
        con = sqlite3.connect('database\\admin.db')
        sql = 'SELECT * FROM admininfo WHERE mail LIKE\'' + mail + '\';'
        cursor = con.execute(sql)
        usermail = ''
        psd = ''
        for row in cursor:
            usermail = row[0]
            psd = row[1]
        if (usermail == ''):
            return school, '-1'
            # 用户名不存在
        elif (psd != password):
            return school, '-1'
        else:
            return school, identity
            # 登陆成功
        con.close()
    elif (identity != '-1'):
        # 学生老师登陆验证
        con = sqlite3.connect('database\\' + school + '.db')
        sql = 'SELECT * FROM %s WHERE mail LIKE\'%s\';' % (identity + 'info', mail)
        cursor = con.execute(sql)
        usermail = ''
        psd = ''
        for row in cursor:
            usermail = row[2]
            psd = row[3]
        if (usermail == ''):
            return school, '-1'
            # 用户名不存在
        elif (psd != password):
            return school, '-1'
            # 密码错误
        else:
            return school, identity
    else:
        return school, '-1'
    con.close()


def get_teacher_infos(school):
    # 用学校名，查询出该学校的所有教师的信息
    # 返回值为一个字典，字典的key为教师 工号； 字典的值为一个list，其中存着: 邮箱， 姓名，手机号
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM teacherinfo;'
    cursor = con.execute(sql)
    teacherinfo = {}
    for row in cursor:
        tid = row[0]
        mail = row[2]
        name = row[1]
        phone = row[4]
        pwd = row[3]
        privilege = row[5]
        teacherinfo[tid] = [mail, name, phone, pwd, privilege]
    con.close()
    return teacherinfo


def query_by(school, id, name, mail):
    # 根据 工号/学号 或者 姓名 或者 邮箱，查询该老师或学生的详细信息
    # 参数有学校才能确定对应的是哪个数据库？
    # 从参数查询老师和学生信息的表格，只要表格中包含参数内的信息，都添加到返回值内
    # 返回值为一个字典，key为工号/学号，value为一个list，其中含有：邮箱，姓名，手机号
    # return {111111: ['haha@sustc.edu.cn', '学生1', '98765432110', 0]}
    info = {}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM teacherinfo WHERE mail LIKE\'%s\' OR name LIKE\'%s\' OR tid LIKE\'%s\';' % (mail, name, id)
    cursor = con.execute(sql)
    for row in cursor:
        tid = row[0]
        mail = row[2]
        name = row[1]
        phone = row[4]
        pwd = row[3]
        privilege = row[5]
        info[tid] = [mail, name, phone, pwd, privilege]
    sql = 'SELECT * FROM studentinfo WHERE mail LIKE\'%s\' OR name LIKE\'%s\' OR sid LIKE\'%s\';' % (mail, name, id)
    cursor = con.execute(sql)
    for row in cursor:
        sid = row[0]
        smail = row[2]
        sname = row[1]
        sphone = row[4]
        spwd = row[3]
        sprivilege = row[5]
        info[sid] = [smail, sname, sphone, spwd, sprivilege]
    con.close()
    return info


def add_teacher(school, tid, name, mail, password, phone, privilege):
    # 添加教师信息，只有手机号是可以非空的，权限是true/false
    # 返回“添加成功”或者“添加失败”
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = '''INSERT INTO "teacherinfo"("tid", "name", "mail","password", "phone", "privilege")''' \
              '''VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''' % (tid, name, mail, password, phone, privilege)
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0


def get_student_infos(school):
    # 用学校名，查询出该学校的所有学生的信息
    # 返回值为一个字典，字典的key为学号； 字典的值为一个list，其中存着: 邮箱， 姓名，手机号
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM studentinfo;'
    cursor = con.execute(sql)
    studentinfo = {}
    for row in cursor:
        tid = row[0]
        mail = row[2]
        name = row[1]
        phone = row[4]
        pwd = row[3]
        privilege = row[5]
        studentinfo[tid] = [mail, name, phone, pwd, privilege]
    con.close()
    return studentinfo


def add_student(school, sid, name, mail, password, phone, privilege):
    # 添加学生信息，只有手机号是可以非空的，权限是true/false
    # 返回“添加成功0”或者“添加失败-1”
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = '''INSERT INTO "studentinfo"("sid", "name", "mail","password", "phone", "privilege")''' \
              '''VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''' % (sid, name, mail, password, phone, privilege)
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0


def modify_student_info(mail, password, phone, school):
    # 修改学生的 密码/电话
    # 这里是共学生页面用的
    # 返回“修改成功0”或者“修改失败-1”
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        if (password != ''):
            sql = 'UPDATE studentinfo SET password = \'%s\' WHERE mail = \'%s\';' % (password, mail)
            con.execute(sql)
            con.commit()
        if (phone != ''):
            sql = 'UPDATE studentinfo SET phone = \'%s\' WHERE mail = \'%s\';' % (phone, mail)
            con.execute(sql)
            con.commit()
    except:
        return -1
    finally:
        con.close()
    return 0


def teacher_modify_infos(school, mail, phone, password):
    # 修改教师的 密码/电话
    # 这里是共教师页面用的
    # 返回“修改成功0”或者“修改失败-1”
    con = sqlite3.connect('database\\' + school + '.db')
    print(phone)
    print(password)
    try:
        sql = 'UPDATE teacherinfo SET phone = \'%s\',password = \'%s\' WHERE mail = \'%s\';' % (phone, password, mail)
        con.execute(sql)
        con.commit()
        # if (password != ''):
        #
        # elif (phone != ''):
        #     sql = 'UPDATE teacherinfo SET phone = \'%s\' WHERE mail = \'%s\';' % (phone, mail)
        #     con.execute(sql)
        #     con.commit()
    except:
        return -1
    finally:
        con.close()
    return 0


def admin_modify_teacher_info(pre_mail, mail, name, password, phone, privilege, school):
    # 修改老师的 密码/电话
    # 返回“修改成功0”或者“修改失败-1”
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = 'UPDATE teacherinfo SET name=\'%s\', mail=\'%s\', password = \'%s\', phone=\'%s\', privilege=\'%s\' WHERE mail = \'%s\';' % (
            name, mail, password, phone, privilege, pre_mail)
        con.execute(sql)
        con.commit()
        # if (password != ''):
        #
        # elif (phone != ''):
        #     sql = 'UPDATE teacherinfo SET phone = \'%s\' WHERE mail = \'%s\';' % (phone, mail)
        #     con.execute(sql)
        #     con.commit()
    except:
        return -1
    finally:
        con.close()
    return 0


def admin_modify_student_info(pre_mail, mail, name, password, phone, privilege, school):
    # 修改学生的 密码/电话
    # 返回“修改成功0”或者“修改失败-1”
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = 'UPDATE studentinfo SET name=\'%s\', mail=\'%s\', password = \'%s\', phone=\'%s\', privilege=\'%s\' WHERE mail = \'%s\';' % (
            name, mail, password, phone, privilege, pre_mail)
        con.execute(sql)
        con.commit()
        # if (password != ''):
        #
        # elif (phone != ''):
        #     sql = 'UPDATE teacherinfo SET phone = \'%s\' WHERE mail = \'%s\';' % (phone, mail)
        #     con.execute(sql)
        #     con.commit()
    except:
        return -1
    finally:
        con.close()
    return 0


def query_student_by_school_mail(school, mail):
    # 这里是根据学校和邮箱，查询特定学生的信息
    # return {'sid': ['11510121@mail.sustc.edu.cn', 'name', 'phone', 'password']}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM studentinfo WHERE mail LIKE\'%s\';' % (mail)
    cursor = con.execute(sql)
    studentinfo = {}
    for row in cursor:
        sid = row[0]
        mail = row[2]
        name = row[1]
        phone = row[4]
        pwd = row[3]
        # privilege = row[5]
        studentinfo[sid] = [mail, name, phone, pwd]
    con.close()
    return studentinfo


def query_course_by(school, cid):
    # 根据课程id返回课程信息
    # 供查询学生选课信息使用
    # return {'cid': ['course_id', 'course_name', 'classroom', 'course_time']}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo WHERE cid = \'%s\';' % (cid)
    cursor = con.execute(sql)
    courseInfo = {}
    for row in cursor:
        cid = row[0]
        cname = row[1]
        classroom = row[4]
        time = row[3]
        courseInfo[cid] = [cid, cname, classroom, time]
    con.close()
    return courseInfo


def query_studentid_by(school, smail):
    # 根据学生邮箱查找学生id
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT*FROM studentinfo WHERE mail LIKE\'%s\';' % (smail)
    cursor = con.execute(sql)
    for row in cursor:
        sid = row[0]
    con.close()
    return sid


def query_student_course(school, mail):
    # 这里是根据学校和学生邮箱，查询该学生的已选课程
    # 这里是供教师页面用
    # return {'sid': ['course_id', 'course_name', 'classroom', 'course_time']}
    # 键值重复，返回值改为[['course_id', 'course_name', 'classroom', 'course_time'],['course_id', 'course_name', 'classroom', 'course_time']]
    sid = query_studentid_by(school, mail)
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM seleCourseInfo WHERE sid = \'%s\';' % (sid)
    cursor = con.execute(sql)
    seleCourse = []
    for row in cursor:
        cid = row[0]
        seleCourse.append(query_course_by(school, cid)[cid])
    con.close()
    return seleCourse


def query_stu_self_course(school, mail):
    # 这里是根据学校和学生邮箱，查询该学生的已选课程
    # 这里是共选课页面用
    # 返回值健有重复  变成了数组[['course_id', 'course_name', 'classroom', 'course_time', 'course_teacher'],['course_id', 'course_name', 'classroom', 'course_time', 'course_teacher']]
    sid = query_studentid_by(school, mail)
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM seleCourseInfo WHERE sid = \'%s\';' % (sid)
    cursor = con.execute(sql)
    seleCourse = []

    for row in cursor:
        cid = row[0]
        seleCourse.append(query_course_by(school, cid)[cid])
    con.close()
    return seleCourse


def query_teachername_by(school, tid):
    # 根据老师id查询老师姓名
    # 课程信息表中的对应关系是cid-tid 防止老师有重名 该方法用在查课程信息时显示老师的名字
    # return teachername
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM teacherinfo WHERE tid LIKE\'%s\';' % (tid)
    cursor = con.execute(sql)
    for row in cursor:
        teachername = row[1]
    con.close()
    return teachername


def query_selectable_courses_by(school, cid, cname, cteacher, ctime, cplace):
    # 参数依次为：课程id, 课程名， 开课教师， 课程时间， 开课地点
    # 可以返回满足任意不为空的参数的课程，也可以返回满足所有不为空的参数的课程
    # return {'cid1': ['cname1', 'cteacher1', 'ctime1', 'cplace1']}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo WHERE cid = \'%s\' OR name = \'%s\' OR tid = \'%s\' OR time = \'%s\'' \
          'OR classroom = \'%s\';' % (cid, cname, cteacher, ctime, cplace)
    cursor = con.execute(sql)
    courseInfo = {}
    for row in cursor:
        cid = row[0]
        cname = row[1]
        tid = row[2]
        tname = query_teachername_by(school, tid)
        time = row[3]
        classroom = row[4]
        courseInfo[cid] = [cname, tname, time, classroom]
    con.close()
    return courseInfo


def query_teacherid_by(school, mail):
    # 根据老师mail查询老师id
    # 返回值为string id
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM teacherinfo WHERE mail LIKE\'%s\';' % (mail)
    cursor = con.execute(sql)
    for row in cursor:
        tid = row[0]
    con.close()
    return tid


def query_selectable_courses(school):
    # 查询该校现在可选课程
    # 返回信息依次有：课程号，开课教师，上课时间，课程地点
    # return {'cid': ['cname', 'cteacher', 'ctime', 'cplace'], 'cid2': ['cname2', 'cteacher2', 'ctime2', 'cplace2']}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo;'
    cursor = con.execute(sql)
    courseinfo = {}
    for row in cursor:
        cid = row[0]
        cname = row[1]
        tid = row[2]
        teacher_name = query_teachername_by(school, tid)
        time = row[3]
        classroom = row[4]
        courseinfo[cid] = [cname, teacher_name, time, classroom]
    con.close()
    return courseinfo


def query_coursename_by(school, cid):
    # 根据课程id 查询课程名
    # 返回string
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo WHERE cid LIKE\'%s\';' % (cid)
    cursor = con.execute(sql)
    for row in cursor:
        cname = row[1]
    con.close()
    return cname


def query_student_scores(school, mail):
    # 根据学校和邮箱，查询该学生已出的成绩
    # 返回一个字典， key为student id；value 为存着课程号，课程名称，该学生对该课程的分数，该学生对该课程的等级（字符串型，且分为：A, B, C, D, P)
    # return {'sid': ['course_id', 'course_name', 'score', 'level']}
    # 返回值有问题 keyc重复  改为数组形式[['course_id', 'course_name', 'score', 'level'],['course_id', 'course_name', 'score', 'level']]
    con = sqlite3.connect('database\\' + school + '.db')
    sid = query_studentid_by(school, mail)
    sql = 'SELECT * FROM scoreinfo WHERE sid LIKE\'%s\';' % (sid)
    cursor = con.execute(sql)
    info = []
    for row in cursor:
        cid = row[0]
        cname = query_coursename_by(school, cid)
        sid = row[1]
        score = row[2]
        level = row[3]
        info.append([cid, cname, score, level])
    con.close()
    return info


def query_teacher_by_school_mail(school, mail):
    # 这里是根据学校和邮箱，查询特定老师的信息
    # return {'tid': ['abc@sustc.edu.cn', 'teachername', 'phone', 'password']}
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM teacherinfo WHERE mail LIKE\'%s\';' % (mail)
    cursor = con.execute(sql)
    teacherinfo = {}
    for row in cursor:
        tid = row[0]
        mail = row[2]
        name = row[1]
        phone = row[4]
        pwd = row[3]
        # privilege = row[5]
        teacherinfo[tid] = [mail, name, phone, pwd]
    con.close()
    return teacherinfo


def query_teacher_course(school, mail):
    # 这里是根据学校和教师邮箱，查询得到该教师发布的课程信息
    # return {'tid': ['course_id', 'course_name', 'classroom', 'course_time', '课程简介']}
    # 返回值改为了数组[['course_id', 'course_name', 'classroom', 'course_time', '课程简介']]
    tid = query_teacherid_by(school, mail)
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo WHERE tid LIKE\'%s\';' % (tid)
    cursor = con.execute(sql)
    courseinfo = []
    for row in cursor:
        cid = row[0]
        cname = row[1]
        time = row[3]
        classroom = row[4]
        introduction = row[5]
        courseinfo.append([cid, cname, classroom, time, introduction])
    con.close()
    return courseinfo


def query_course_student(school, mail):
    # 这里是根据学校和教师邮箱，查询得到该教师发布的所有课程分别对应的选课学生
    # 返回一个字典，key为课程号，value一个字符串，里面是所有选课学生的学号（注意：字符串的最后面没有逗号）
    # return {'course_id': 'sid1, sid2, sid3'}
    tid = query_teacherid_by(school, mail)
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM courseinfo WHERE tid LIKE\'%s\';' % (tid)
    cursor = con.execute(sql)
    courses = []
    info = {}
    for row in cursor:
        cid = row[0]
        courses.append(cid)
    for index in range(0, len(courses)):
        sql = 'SELECT * FROM seleCourseInfo WHERE cid LIKE\'%s\';' % (courses[index])
        cursor = con.execute(sql)
        s = ''
        for row in cursor:
            sid = row[1]
            s = s + ',' + sid
        info[index] = s[1:]
    con.close()
    return info


def query_studentname_by(school, sid):
    # 根据学生学号查询学生姓名
    # 返回值为string
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM studentinfo WHERE sid LIKE\'%s\';' % (sid)
    cursor = con.execute(sql)
    for row in cursor:
        sname = row[1]
    con.close()
    return sname


def get_course_student_score(school, teacher_mail):
    # 这里的返回结果有点复杂
    # 返回结果形如：{ [course_id, course_name]: { student_id: [student_name, score, level] } }
    # 作用是查出该教师开设的所有课程对应的学生成绩
    # return {('course1', 'cname1'): {'student1': ['stuname1', '90', 'A'], 'student2': ['stuname2', '85', 'B']}, ('course2', 'cname2'): {'student3': ['stuname3', '93', 'A']}}
    allcourses = query_teacher_course(school, teacher_mail)
    con = sqlite3.connect('database\\' + school + '.db')
    courseinfo = {}
    for index in range(0, len(allcourses)):
        studentinfo = {}
        cid = allcourses[index][0]
        cname = allcourses[index][1]
        sql = 'SELECT * FROM scoreinfo WHERE cid LIKE\'%s\';' % (cid)
        cursor = con.execute(sql)
        for row in cursor:
            sid = row[1]
            sname = query_studentname_by(school, sid)
            score = row[2]
            level = row[3]
            studentinfo[sid] = [sname, score, level]
        courseinfo[(cid, cname)] = studentinfo
    con.close()
    return courseinfo


def add_course_by_teacher(school, mail, course):
    # 参数为：学校 string， 教师邮箱 string, 课程信息 list
    # course的结构为：[courseid, coursename, coursetime, classroom, courseintroduction]
    # 这里是教师添加课程的操作，添加成功则返回 0， 添加失败则返回 -1
    tid = query_teacherid_by(school, mail)
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = '''INSERT INTO "courseinfo"("cid", "name", "tid","time", "classroom", "introduction")''' \
              '''VALUES ('%s', '%s', '%s', '%s', '%s', '%s');''' % (
                  course[0], course[1], tid, course[2], course[3], course[4])
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0


def add_stu_score(school, teacher_mail, sid, cid, score, level):
    # 参数依次为：学校，教师邮箱，学生学号，课程号，分数，等级（字符串型的 A, B, C, D, P)
    # 若添加成功，返回 0， 若添加失败， 返回 -1
    con = sqlite3.connect('database\\' + school + '.db')
    try:
        sql = '''INSERT INTO "scoreinfo"("cid", "sid", "score", "level")''' \
              '''VALUES ('%s', '%s', '%s', '%s');''' % (cid, sid, score, level)
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0


def query_student_score(school, sid, sname, cid, cname):
    # 参数依次为：学校， 学生学号， 学生姓名，课程号，课程名
    # 如果能实现模糊查询比较好
    # 需要返回满足条件的一个字典，字典结构形如：{course_id: {student_id:[ student_name, score, level]}}
    # return {('course1', 'cname1'): {'student1': ['stuname1', '90', 'A'], 'student2': ['stuname2', '85', 'B']},
    #        ('course2', 'cname2'): {'student3': ['stuname3', '93', 'A']}}
    con = sqlite3.connect('database\\' + school + '.db')
    info = {}
    sql = '''SELECT * FROM courseinfo WHERE name LIKE'%%%s%%' OR cid = '%s' ;''' % (cname, cid)
    cursor = con.execute(sql)
    courses = []
    for row in cursor:
        courses.append(row[0])
    sql = 'SELECT * FROM studentinfo WHERE sid = \'%s\' OR name LIKE\'%%%s%%\' ;' % (sid, sname)
    cursor = con.execute(sql)
    students = []
    for row in cursor:
        students.append(row[0])
    for index in range(0, len(courses)):
        for j in range(0, len(students)):
            sql = 'SELECT * FROM scoreinfo WHERE cid = \'%s\' AND sid = \'%s\';' % (courses[index], students[j])
            cursor = con.execute(sql)
            for row in cursor:
                cid = row[0]
                cname = query_coursename_by(school, cid)
                sid = row[1]
                sname = query_studentname_by(school, sid)
                score = row[2]
                level = row[3]
            if (cid, cname) in info:
                dic = info.get((cid, query_coursename_by(school, cid)))
                dic[sid] = [sname, score, level]
                info[(cid, query_coursename_by(school, cid))] = dic
            else:
                info[(cid, query_coursename_by(school, cid))] = {sid: [sname, score, level]}
    return info


def student_withdraw_course(school, student_mail, course_id):
    # 学生退课操作。使用student_id或student_mail作为索引
    # 成功返回0， 失败返回-1
    print(student_mail)
    print(school)
    print(course_id)
    con = sqlite3.connect('database\\' + school + '.db')
    sid = query_studentid_by(school, student_mail)
    try:
        sql = 'DELETE FROM seleCourseInfo  WHERE sid = \'%s\' AND cid = \'%s\';' % (sid, course_id)
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0


def course_students(school, cid):
    con = sqlite3.connect('database\\' + school + '.db')
    sql = 'SELECT * FROM seleCourseInfo WHERE cid LIKE\'%s\';' % (cid)
    cursor = con.execute(sql)
    students = []
    for row in cursor:
        sid = row[1]
        students.append(sid)
    con.close()
    return students


def student_choose_course(school, smail, cid):
    # 学生选课操作
    # 成功返回0， 失败返回-1
    sid = query_studentid_by(school, smail)
    con = sqlite3.connect('database\\' + school + '.db')
    students = course_students(school, cid)
    for index in range(0, len(students)):
        if students[index] == sid:
            return -1
        else:
            pass
    try:
        sql = '''INSERT INTO "seleCourseInfo"("cid", "sid")''' \
              '''VALUES ('%s', '%s');''' % (cid, sid)
        con.execute(sql)
    except:
        return -1
    else:
        con.commit()
        con.close()
        return 0
