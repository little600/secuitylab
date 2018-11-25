from flask import render_template, session, request, redirect, url_for
from app import app
from app import functions


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/logincheck',methods=['POST','GET'])
def logincheck():
    if request.method=='POST':
      if request.form['username']=='guest'and request.form['password']=='guest':
         session['login']='true'
         return redirect(url_for('mylab'))
      else:
          session['login_error'] = '用户名和密码不正确，访客请使用guest登录'
          return redirect(url_for('login'))

@app.route('/joincheck',methods=['POST','GET'])
def joincheck():
    if request.method=='POST':
      if request.form['invite']==functions.get_invite_code(request.form['username']):
          session['join_error'] = '注册成功！'
          return redirect(url_for('join'))
      else:
          session['join_error'] = '邀请码不正确'
          return redirect(url_for('join'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/login')
def login(error=None):
    if 'login_error'in session:
        error=session['login_error']
    if 'login'in session:
        return redirect(url_for('mylab'))
    else:
        return render_template('login.html',error=error)


@app.route('/join')
def join(error=None):
    if 'join_error'in session:
        error=session['join_error']
        return render_template('join.html',error=error)
    else:
        return render_template('join.html', error=error)


@app.route('/mylab')
def mylab():
    if 'login'in session:
        if 'lab_id' in session:
            return render_template('mylab.html', lab_id=session['lab_id'], web_add='10.158.68.200:' + str(session['web_port']), vnc_add=str(session['vnc_port']), ssh_add=str(session['ssh_port']), loading='none',sleep_time=0)
        else:
            web_port = functions.getPort('web_port')
            functions.sleep()
            vnc_port = functions.getPort('vnc_port')
            functions.sleep()
            ssh_port = functions.getPort('ssh_port')
            functions.sleep()
            lab_id = functions.docker_control('run', web_port, vnc_port, ssh_port)
            session['lab_id'] = lab_id
            session['web_port'] = web_port
            session['vnc_port'] = vnc_port
            session['ssh_port'] = ssh_port
            return render_template('mylab.html', lab_id=lab_id, web_add='10.158.68.200:' + str(web_port), vnc_add=str(vnc_port), ssh_add=str(ssh_port), loading='',sleep_time=functions.random.randint(10000, 15000))
    else:
        session['error']='请登录系统'
        return redirect(url_for('login'))


@app.route('/courses')
def courses():
    if 'courses_lab_id' in session:
        return render_template('courses_layout.html', courses_desktop='http://10.158.68.200:' + str(session['courses_web_port']), loading='none', sleep_time=0)
    else:
        web_port = functions.getPort('web_port')
        functions.sleep()
        vnc_port = functions.getPort('vnc_port')
        functions.sleep()
        ssh_port = functions.getPort('ssh_port')
        functions.sleep()
        courses_lab_id = functions.docker_control('run', web_port, vnc_port, ssh_port)
        session['courses_lab_id']=courses_lab_id
        session['courses_web_port']=web_port
        return render_template('courses_layout.html', courses_desktop='http://10.158.68.200:' + str(web_port), loading='', sleep_time=functions.random.randint(10000, 15000))

