from flask import Flask,render_template,request,redirect,url_for,send_file
from flask_login import login_user,UserMixin,LoginManager,login_required,logout_user,current_user
import datetime
import os
import sys
import pandas as pd
import time
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
app = Flask(__name__)
app.template_folder = 'template'
app.secret_key='12344'
delta=datetime.timedelta(days=1)
login_manager=LoginManager(app)
# login_manager.login_view='test'

class User(UserMixin):
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    print (user_id)
    if(int(user_id)==1):
        return User(1,'yxp','123')
    elif(int(user_id)==2):
        return User(2,'xp','123')
    else:
        return None

@app.route('/word')
@login_required
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/yxp')
@login_required
def hello_world2():  # put application's code here
    print (current_user.id)
    print (current_user.get_id())
    return 'Hello yxp!'


@app.route('/test')
def template():  # put application's code here
    return render_template('demo.html')


@app.route('/login',methods=['POST'])
def login():  # put application's code here
    username=request.form.get('username')
    password=request.form.get('password')
    if(username=='yxp' and password=='123'):
        user = User(1,username,password)
        logout_user()
        login_user(user,True,datetime.timedelta(days=1))
        return {'code':200}
    elif(username=='xp' and password=='123'):
        user = User(2,username,password)
        logout_user()
        login_user(user,True,datetime.timedelta(days=1))
        return {'code':200}
    else:
        return {'mesage':'password invalid','code':500}



@app.route('/index')
def index():  # put application's code here    
    return render_template('index.html')


@app.route('/file_submit',methods=['POST'])
def file_submit():  # put application's code here    
    file=request.files.get('before')
    time_before = int(time.time())
    time_now = int(time.time())
    name1='before_{}.csv'.format(time_before)
    name2='now_{}.csv'.format(time_now)
    if file:
        file.save(name1)
    else:
        return '上传失败'
    file=request.files.get('after')
    if file:
        file.save(name2)
    else:
        return '上传失败'
    data1=pd.read_csv(name1,encoding="utf-8",engine="python")
    data2=pd.read_csv(name2,encoding="utf-8",engine="python")

    result=pd.merge(data1,data2,how="left",on=['成员'],suffixes=('_before', '_now'))
    result['贡献排名变化']=result[' 贡献排行_now']-result[' 贡献排行_before']
    result['战功总量变化']=result[' 战功总量_now']-result[' 战功总量_before']
    result['势力值变化']=result[' 势力值_now']-result[' 势力值_before']
    result['贡献总量变化']=result[' 贡献总量_now']-result[' 贡献总量_before']
    f=result.sort_values('贡献总量变化',ascending=False)
    finalname='final_{}.csv'.format(int(time.time()))
    f.to_csv(finalname,index=1, encoding='utf_8_sig')
    return send_file(finalname, as_attachment=True)





if __name__ == '__main__':
    app.run()