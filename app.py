# -*- coding: utf-8 -*-
import os
from flask import jsonify, Flask, request, session, g, redirect, request, url_for, abort, render_template, flash, \
    make_response
from jinja2 import Template
from flask_sijax import sijax
import utils as utl

# path = os.path.join('.', os.path.dirname(__file__), 'static/sijax')
app = Flask(__name__)
# app.config['SIJAX_STATIC_PATH'] = path
# app.config['SIJAX_JSON_URI'] = '/static/sijax/json2.js'
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'

cookie_key = 'user_school'
SERVICES = 'services'
INFO_SERVICE = 'info_service'
COURSE_SERVICE = 'course_service'
SCORE_SERVICE = 'score_service'


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/buy_info_service/', methods=['POST', 'GET'])
def buy_info_service():
    print('收到购买请求')
    user_name, school = from_cookie_get_username_school(request)
    print(user_name)
    print(school)
    success = utl.buy_info_service(school, user_name)
    return success


@app.route('/buy_score_service/', methods=['POST', 'GET'])
def buy_score_service():
    user_name, school = from_cookie_get_username_school(request)
    success = utl.buy_score_service(school, user_name)
    return success


@app.route('/buy_course_service/', methods=['POST', 'GET'])
def buy_course_service():
    user_name, school = from_cookie_get_username_school(request)
    success = utl.buy_course_service(school, user_name)
    return success


def get_admin(user_name, school, teacher_result={}, student_result={}, admin_query_result={}):
    services = get_services(user_name)
    info_days, course_days, score_days = utl.get_days(school)
    return make_response(render_template('admin.html', teacher_result=teacher_result, student_result=student_result,
                                         admin_query_result=admin_query_result, INFO_SERVICE=services[INFO_SERVICE],
                                         COURSE_SERVICE=services[COURSE_SERVICE],
                                         SCORE_SERVICE=services[SCORE_SERVICE], info_days=info_days,
                                         score_days=score_days, course_days=course_days))


def get_default_admin(school, user_name):
    teacher_infos = utl.get_teacher_infos(school)
    student_infos = utl.get_student_infos(school)
    admin_rsp = get_admin(user_name, school, teacher_result=teacher_infos, student_result=student_infos)
    return admin_rsp


@app.route('/admin/', methods=['POST', 'GET'])
def admin(school, user_name):
    if user_name in session:
        print('成功登录')
    else:
        return redirect(url_for('index'))
    teacher_infos = utl.get_teacher_infos(school)
    student_infos = utl.get_student_infos(school)
    admin_rsp = get_admin(user_name, school, teacher_result=teacher_infos, student_result=student_infos)
    # admin_rsp.set_cookie(user_name, school)
    cookie_value = str(user_name) + '+' + str(school)
    admin_rsp.set_cookie(cookie_key, cookie_value)
    return admin_rsp


def get_student(user_name, student_self={}, student_course={},
                student_scores={}):
    services = get_services(user_name)
    return make_response(
        render_template('student.html', INFO_SERVICE=services[INFO_SERVICE], student_self=student_self,
                        COURSE_SERVICE=services[COURSE_SERVICE],
                        student_course=student_course, SCORE_SERVICE=services[SCORE_SERVICE],
                        student_scores=student_scores))


def get_services(user_name):
    services_pre = session[user_name][SERVICES]
    services = {}
    if services_pre[INFO_SERVICE] == 'true':
        services[INFO_SERVICE] = True
    else:
        services[INFO_SERVICE] = False
    if services_pre[COURSE_SERVICE] == 'true':
        services[COURSE_SERVICE] = True
    else:
        services[COURSE_SERVICE] = False
    if services_pre[SCORE_SERVICE] == 'true':
        services[SCORE_SERVICE] = True
    else:
        services[SCORE_SERVICE] = False
    return services


def get_default_student(user_name, school):
    services = get_services(user_name)
    if services[INFO_SERVICE]:
        self_info = utl.query_student_by_school_mail(school, user_name)
    else:
        self_info = {}
    if services[COURSE_SERVICE]:
        stu_courses = utl.query_student_course(school, user_name)
    else:
        stu_courses = {}
    if services[SCORE_SERVICE]:
        stu_scores = utl.query_student_scores(school, user_name)
    else:
        stu_scores = {}
    student_rsp = get_student(user_name, student_self=self_info,
                              student_course=stu_courses,
                              student_scores=stu_scores)
    return student_rsp


@app.route('/student/', methods=['POST', 'GET'])
def student(school, user_name):
    if user_name in session:
        print('成功登录')
    else:
        return redirect(url_for('index'))
    services = get_services(user_name)
    if services[INFO_SERVICE]:
        self_info = utl.query_student_by_school_mail(school, user_name)
    else:
        self_info = {}
    if services[COURSE_SERVICE]:
        stu_courses = utl.query_student_course(school, user_name)
    else:
        stu_courses = {}
    if services[SCORE_SERVICE]:
        stu_scores = utl.query_student_scores(school, user_name)
    else:
        stu_scores = {}
    student_rsp = get_student(user_name, student_self=self_info,
                              student_course=stu_courses,
                              student_scores=stu_scores)
    cookie_value = str(user_name + '+' + str(school))
    student_rsp.set_cookie(cookie_key, cookie_value)
    return student_rsp


def get_teacher(user_name, teacher_self={}, teacher_course={}, course_student={}, query_course_student_score={},
                course_student_score={}):
    services = get_services(user_name)
    return make_response(
        render_template('teacher.html', teacher_self=teacher_self, teacher_course=teacher_course,
                        course_student=course_student, query_course_student_score=query_course_student_score,
                        course_student_score=course_student_score, INFO_SERVICE=services[INFO_SERVICE],
                        COURSE_SERVICE=services[COURSE_SERVICE], SCORE_SERVICE=services[SCORE_SERVICE]))


def get_default_teacher(school, user_name):
    teacher_self_info = utl.query_teacher_by_school_mail(school, user_name)
    teacher_course = utl.query_teacher_course(school, user_name)
    course_student = utl.query_course_student(school, user_name)
    course_student_score = utl.get_course_student_score(school, user_name)
    teacher_rsp = get_teacher(user_name, teacher_self=teacher_self_info, teacher_course=teacher_course,
                              course_student=course_student, course_student_score=course_student_score)
    return teacher_rsp


@app.route('/teacher/', methods=['POST', 'GET'])
def teacher(school, user_name):
    if user_name in session:
        print('成功登录')
    else:
        return redirect(url_for('index'))
    teacher_self_info = utl.query_teacher_by_school_mail(school, user_name)
    teacher_course = utl.query_teacher_course(school, user_name)
    course_student = utl.query_course_student(school, user_name)
    course_student_score = utl.get_course_student_score(school, user_name)
    teacher_rsp = get_teacher(user_name, teacher_self=teacher_self_info, teacher_course=teacher_course,
                              course_student=course_student, course_student_score=course_student_score)
    cookie_value = str(user_name + '+' + str(school))
    teacher_rsp.set_cookie(cookie_key, cookie_value)
    return teacher_rsp


@app.route('/upload_stu_score/', methods=['POST', 'GET'])
def upload_stu_score():
    user_name, school = from_cookie_get_username_school(request)
    form = request.form
    sid = form['sid']
    cid = form['cid']
    score = form['score']
    level = form['level']
    add_result = utl.add_stu_score(school, user_name, sid, cid, score, level)
    return teacher(school, user_name)


@app.route('/add_course/', methods=['POST', 'GET'])
def add_course():
    user_name, school = from_cookie_get_username_school(request)
    form = request.form
    id = form['course_id']
    name = form['course_name']
    time = form['course_time']
    classroom = form['classroom']
    intro = form['course_intro']
    course = [id, name, time, classroom, intro]
    add_result = utl.add_course_by_teacher(school, user_name, course)

    # teacher_self_info = utl.query_teacher_by_school_mail(school, user_name)
    # teacher_course = utl.query_teacher_course(school, user_name)
    # course_student = utl.query_course_student(school, user_name)

    # return render_template('teacher.html', teacher_self=teacher_self_info, teacher_course=teacher_course,
    #                        course_student=course_student)
    return teacher(school, user_name)


@app.route('/query_stu_score/', methods=['POST', 'GET'])
def query_stu_score():
    user_name, school = from_cookie_get_username_school(request)
    form = request.form
    sid = form['sid']
    sname = form['sname']
    cid = form['cid']
    cname = form['cname']

    query_course_student_score = utl.query_student_score(school, sid, sname, cid, cname)
    course_student_score = utl.get_course_student_score(school, user_name)

    teacher_self_info = utl.query_teacher_by_school_mail(school, user_name)
    teacher_course = utl.query_teacher_course(school, user_name)
    course_student = utl.query_course_student(school, user_name)

    return get_teacher(user_name, teacher_self=teacher_self_info, teacher_course=teacher_course,
                       course_student=course_student, query_course_student_score=query_course_student_score,
                       course_student_score=course_student_score)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    # 11510082@mail.sustc.edu.cn
    mail = request.form['mail']
    print(mail)
    pwd = request.form['password']
    print(pwd)
    school, identity = utl.login_match(mail, pwd)
    print(identity)

    if identity == '-1':
        return redirect(url_for('index'))
    else:
        info_service, course_service, score_service = utl.get_services(school)
        session[mail] = {'password': pwd, SERVICES: {INFO_SERVICE: info_service, COURSE_SERVICE: course_service,
                                                     SCORE_SERVICE: score_service}}
        if identity == 'admin':
            resp = admin(user_name=mail, school=school)
            return resp
            # return redirect(url_for('admin', user_name=mail, school=school))
        elif identity == 'student':
            resp = student(user_name=mail, school=school)
            return resp
        elif identity == 'teacher':
            resp = teacher(user_name=mail, school=school)
            return resp

    return redirect(url_for('index'))


@app.route('/admin/query/', methods=['POST', 'GET'])
def query():
    form = request.form
    id = form['id']
    name = form['name']
    mail = form['mail']
    user_name, school = from_cookie_get_username_school(request)
    oneinfo = utl.query_by(school, id, name, mail)

    teacher_infos = utl.get_teacher_infos(school)
    student_infos = utl.get_student_infos(school)
    admin_rsp = get_admin(user_name, school, teacher_result=teacher_infos, student_result=student_infos,
                          admin_query_result=oneinfo)

    return admin_rsp


def from_cookie_get_username_school(request):
    cookie = request.cookies.get(cookie_key)
    uns = cookie.split("+")
    return uns[0], uns[1]


@app.route('/add_teacher_student/', methods=['POST', 'GET'])
def add_teacher_student():
    print("admin添加行为")
    user_name, school = from_cookie_get_username_school(request)

    form = request.form
    id = form['id']
    print(id)
    name = form['name']
    print(name)
    mail = form['mail']
    print(mail)
    phone = form['phone']
    print(phone)
    pwd = form['password']
    print(pwd)
    previlige = form['privilege']
    print(previlige)
    who = form['who']
    if who == 'teacher':
        utl.add_teacher(school, id, name, mail, pwd, phone, previlige)
    elif who == 'student':
        utl.add_student(school, id, name, mail, pwd, phone, previlige)

    teacher_infos = utl.get_teacher_infos(school)
    student_infos = utl.get_student_infos(school)

    admin_rsp = get_admin(user_name, school, teacher_result=teacher_infos, student_result=student_infos)

    return admin_rsp


@app.route('/logout/<string:mail>')
def logout(mail):
    session.pop(mail, None)
    return redirect(url_for(index))


def get_course_sys(my_courses_result, query_courses_result, courses_result):
    return make_response(render_template('course_sys.html', my_courses_result=my_courses_result,
                                         query_courses_result=query_courses_result, courses_result=courses_result))


@app.route('/course_sys/', methods=['GET', 'POST'])
def course_sys():
    smail, school = from_cookie_get_username_school(request)
    my_courses_result = utl.query_stu_self_course(school=school, mail=smail)
    query_courses_result = {}
    courses_result = utl.query_selectable_courses(school)

    return get_course_sys(my_courses_result=my_courses_result,
                          query_courses_result=query_courses_result, courses_result=courses_result)


@app.route('/csys_query/', methods=['GET', 'POST'])
def csys_query():
    smail, school = from_cookie_get_username_school(request)

    form = request.form
    cid = form['cid']
    cname = form['cname']
    cteacher = form['cteacher']
    ctime = form['ctime']
    cplace = form['cplace']

    query_courses_result = utl.query_selectable_courses_by(school, cid, cname, cteacher, ctime, cplace)
    my_courses_result = utl.query_stu_self_course(school=school, mail=smail)
    courses_result = utl.query_selectable_courses(school)
    return get_course_sys(my_courses_result=my_courses_result, query_courses_result=query_courses_result,
                          courses_result=courses_result)


def get_identity(mail):
    atindex = mail.find('@')
    postfix = mail[atindex + 1: len(mail)]
    postfix_splite = postfix.split(".")
    if (len(postfix_splite) == 4):
        identity = 'student'
    elif (postfix_splite[len(postfix_splite) - 2] == 'edu'):
        identity = 'teacher'
    elif (postfix_splite[len(postfix_splite) - 2] == 'adm'):
        identity = 'admin'
    else:
        identity = '-1'
    return identity


@app.route('/admin_modify/', methods=['POST', 'GET'])
def admin_modify():
    print('收到修改request')
    mail, school = from_cookie_get_username_school(request)
    print(mail)
    print(school)

    mmail = request.values['mmail']
    mname = request.values['mname']

    mphone = request.values['mphone']
    mpwd = request.values['mpwd']
    mprivilege = request.values['mprivilege']
    print(mmail)
    print(mname)
    print(mprivilege)
    # if mprivilege == '限制':
    #     mprivilege = 'false'
    # elif mprivilege == '不限制':
    #     mprivilege = 'true'

    identity = get_identity(mmail)
    if identity == 'student':
        sucess = utl.admin_modify_student_info(mail, mmail, mname, mpwd, mphone, mprivilege, school)
    elif identity == 'teacher':
        sucess = utl.admin_modify_teacher_info(mail, mmail, mname, mpwd, mphone, mprivilege, school)
    print(sucess)

    return get_default_admin(school, mail)


@app.route('/student_modify/', methods=['POST', 'GET'])
def student_modify():
    print('收到修改请求')
    user_name, school = from_cookie_get_username_school(request)
    mphone = request.values['mphone']
    mpwd = request.values['mpwd']
    print(mphone)
    print(mpwd)
    success = utl.modify_student_info(user_name, mpwd, mphone, school)
    return get_default_student(user_name, school)


@app.route('/student_withdraw_course/', methods=['POST', 'GET'])
def student_withdraw_course():
    print('收到退课请求')
    user_name, school = from_cookie_get_username_school(request)
    cid = request.values['course_id']
    success = utl.student_withdraw_course(school, user_name, cid)

    return get_default_student(user_name, school)


@app.route('/student_choose_course/', methods=['POST', 'GET'])
def student_choose_course():
    print('收到选课请求')
    user_name, school = from_cookie_get_username_school(request)
    cid = request.values['course_id']
    success = utl.student_choose_course(school, user_name, cid)

    return get_default_student(user_name, school)


@app.route('/teacher_modify/', methods=['POST', 'GET'])
def teacher_modify():
    tmail, school = from_cookie_get_username_school(request)
    mphone = request.values['mphone']
    mpwd = request.values['mpwd']
    success = utl.teacher_modify_infos(school, tmail, mphone, mpwd)

    return get_default_teacher(school, tmail)


if __name__ == '__main__':
    app.run()
