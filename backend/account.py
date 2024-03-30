from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO
import json
import pytz
import threading
import time_cal
from datetime import datetime
import time
from sqlalchemy import or_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 資料庫樣式
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StreamerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataType = db.Column(db.String(2000))
    DiscordUsername = db.Column(db.String(2000))
    MinecraftName = db.Column(db.String(2000))
    Email = db.Column(db.String(2000))
    Duration = db.Column(db.String(2000))
    Position = db.Column(db.String(2000))
    Nickname = db.Column(db.String(2000))
    ChannelUrl = db.Column(db.String(2000))
    Works = db.Column(db.String(2000))
    Motivation = db.Column(db.String(2000))
    DesiredMember = db.Column(db.String(2000))
    PostApprovalActivity = db.Column(db.String(2000))
    SelfIntroduction = db.Column(db.String(2000))
    SubmitTime = db.Column(db.String(2000))
    Tag = db.Column(db.String(200000))
    Viewed = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            "id": self.id,
            "dataType": self.dataType,
            "DiscordUsername": self.DiscordUsername,
            "MinecraftName": self.MinecraftName,
            "Email": self.Email,
            "Duration": self.Duration,
            "Position": self.Position,
            "Nickname": self.Nickname,
            "ChannelUrl": self.ChannelUrl,
            "Works": self.Works,
            "Motivation": self.Motivation,
            "DesiredMember": self.DesiredMember,
            "PostApprovalActivity": self.PostApprovalActivity,
            "SelfIntroduction": self.SelfIntroduction,
            "SubmitTime": self.SubmitTime,
            "Tag": self.Tag,
            "Viewed": self.Viewed
        }
    
class WingmanInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataType = db.Column(db.String(2000))
    DiscordUsername = db.Column(db.String(2000))
    MinecraftName = db.Column(db.String(2000))
    Email = db.Column(db.String(2000))
    Duration = db.Column(db.String(2000))
    Position = db.Column(db.String(2000))
    Nickname = db.Column(db.String(2000))
    Motivation = db.Column(db.String(2000))
    ClosestMember = db.Column(db.String(2000))
    MemberDuration = db.Column(db.String(2000))
    SelfIntroduction = db.Column(db.String(2000))
    SubmitTime = db.Column(db.String(2000))
    Tag = db.Column(db.String(200000))
    Viewed = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "dataType": self.dataType,
            "DiscordUsername": self.DiscordUsername,
            "MinecraftName": self.MinecraftName,
            "Email": self.Email,
            "Duration": self.Duration,
            "Position": self.Position,
            "Nickname": self.Nickname,
            "Motivation": self.Motivation,
            "ClosestMember": self.ClosestMember,
            "SelfIntroduction": self.SelfIntroduction,
            "SubmitTime": self.SubmitTime,
            "Tag": self.Tag,
            "Viewed": self.Viewed
        }

class RenewerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataType = db.Column(db.String(2000))
    DiscordUsername = db.Column(db.String(2000))
    MinecraftName = db.Column(db.String(2000))
    Email = db.Column(db.String(2000))
    Duration = db.Column(db.String(2000))
    Position = db.Column(db.String(2000))
    Renewer_nickname = db.Column(db.String(2000))
    SubmitTime = db.Column(db.String(2000))
    Tag = db.Column(db.String(200000))
    Viewed = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "dataType": self.dataType,
            "DiscordUsername": self.DiscordUsername,
            "MinecraftName": self.MinecraftName,
            "Email": self.Email,
            "Duration": self.Duration,
            "Position": self.Position,
            "Renewr_nickname":self.Renewer_nickname,
            "SubmitTime": self.SubmitTime,
            "Tag": self.Tag,
            "Viewed": self.Viewed    
        }
    
class MemberInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DiscordUsername = db.Column(db.String(2000))
    DiscordUserID = db.Column(db.String(2000))
    MinecraftName = db.Column(db.String(2000))
    Position = db.Column(db.String(2000))
    PassTime = db.Column(db.String(2000))
    Email = db.Column(db.String(2000))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/superadmin')
@login_required
def superadmin():
    if not current_user.role == 'superadmin':
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('superadmin.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.role == 'superadmin':
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('superadmin'))



def create_superadmin():
    superadmin = User.query.filter_by(username='zou').first()
    if not superadmin:
        superadmin = User(username='zou', role='superadmin')
        superadmin.set_password('123456789')
        db.session.add(superadmin)
        db.session.commit()

@app.route('/assign_manager/<int:user_id>', methods=['POST'])
@login_required
def assign_manager(user_id):
    if not current_user.role == 'superadmin':
        return redirect(url_for('index'))  # 只有 superadmin 可以分配角色
    user = User.query.get_or_404(user_id)
    user.role = 'manager'
    db.session.commit()
    flash('Assigned Manager role successfully.')
    return redirect(url_for('superadmin'))


@app.route('/manager_dashboard')
@login_required
def manager_dashboard():
    if current_user.role not in ['manager', 'superadmin']:
        return redirect(url_for('index'))  # 或者返回一個錯誤頁面
    # 這裏實現顯示給 manager 和 superadmin 的儀表板邏輯
    return render_template('manager_dashboard.html')





@app.route('/store', methods=['POST'])
def store_data():
    data = request.json
    data['Tag'] = increment_counter()
    data['Viewed'] = "no"
    print(data)
    if data['dataType'] == 'streamer':
        new_entry = StreamerInfo(**data)
        db.session.add(new_entry)
    elif data['dataType'] == 'wingman':
        new_entry = WingmanInfo(**data)
        db.session.add(new_entry)
    elif data['dataType'] == 'renewer':
        new_entry = RenewerInfo(**data)
        db.session.add(new_entry)
    else:
        return jsonify({"error": "Unsupported dataType"}), 400
    
    db.session.commit()
    return jsonify({"message": "Data stored successfully"}), 201




def query_info():
    streamer_infos = StreamerInfo.query.with_entities(StreamerInfo.Position, StreamerInfo.Email, StreamerInfo.SubmitTime, StreamerInfo.Tag, StreamerInfo.Viewed).all()
    wingman_infos = WingmanInfo.query.with_entities(WingmanInfo.Position, WingmanInfo.Email, WingmanInfo.SubmitTime, WingmanInfo.Tag, WingmanInfo.Viewed).all()
    renewer_infos = RenewerInfo.query.with_entities(RenewerInfo.Position, RenewerInfo.Email, RenewerInfo.SubmitTime, RenewerInfo.Tag, RenewerInfo.Viewed).all()
    print(streamer_infos,wingman_infos,renewer_infos)
    return streamer_infos, wingman_infos, renewer_infos

@app.route('/get_info')
def get_info():

    streamer_infos, wingman_infos, renewer_infos = query_info()
    start_time_get_info, end_time_get_info = compare_time(gap_day_remind, next_gap_day_return)
    def transform(results):
        utc_zone = pytz.utc
        taiwan_zone = pytz.timezone('Asia/Taipei')
        filtered_results = []
        print(start_time_get_info,  end_time_get_info)
        for item in results:
            tran_submit_time_to_compare = datetime.fromisoformat(item[2].replace('Z','+00:00')).replace(tzinfo=utc_zone)
            tran_submit_time_to_compare_taiwan = tran_submit_time_to_compare.astimezone(taiwan_zone)
            tran_submit_time_to_compare_naive = tran_submit_time_to_compare_taiwan.replace(tzinfo=None) # 移除時區資訊
            test_Viewed = item[4]
            if  start_time_get_info < tran_submit_time_to_compare_naive < end_time_get_info and test_Viewed == "no":
                filtered_results.append(dict(Position=item[0], Email=item[1], SubmitTime=item[2], Tag=item[3]))
        return filtered_results
    

    data = {
        "streamers": transform(streamer_infos),
        "wingmans": transform(wingman_infos),
        "renewers": transform(renewer_infos)
    }
    return jsonify(data)





def compare_time(end_time_to_compare ,strat_date_to_compare):
    strat_date_to_compare_str = str(strat_date_to_compare)
    tran_end_time_to_compare = datetime.strptime(end_time_to_compare, "%Y/%m/%d")
    tran_strat_date_to_compare = datetime.strptime(strat_date_to_compare_str , "%Y-%m-%d %H:%M:%S")
    return tran_end_time_to_compare, tran_strat_date_to_compare

data_sequence_file = 'C:/Users/User/Desktop/management_system/backend/json/data_sequence.json'

def read_counter():
    """從JSON檔案讀取計數器的值"""
    try:
        with open(data_sequence_file, 'r') as file:
            data = json.load(file)
            return data.get('count', 0)
    except FileNotFoundError:
        return 0

def save_counter(count):
    """將計數器的值儲存到JSON檔案"""
    with open(data_sequence_file, 'w') as file:
        json.dump({'count': count}, file)


def increment_counter():
    """增加計數器的值"""
    count = read_counter() + 1
    save_counter(count)
    return count




@app.route('/query_tag', methods=['GET'])
@login_required
def query_tag():
    tag = request.args.get('tag')
    if current_user.role not in ['manager', 'superadmin']:
        return render_template('no_permission.html')
    elif not tag:
        return jsonify({"error": "Tag parameter is required"}), 400
    else:
        streamer_infos_all = StreamerInfo.query.filter_by(Tag=tag).all()
        wingman_infos_all = WingmanInfo.query.filter_by(Tag=tag).all()
        renewer_infos_all = RenewerInfo.query.filter_by(Tag=tag).all()
        
        data = {}
        
        if streamer_infos_all:
            data["streamers"] = [item.to_dict() for item in streamer_infos_all]
        if wingman_infos_all:
            data["wingmans"] = [item.to_dict() for item in wingman_infos_all]
        if renewer_infos_all:
            data["renewers"] = [item.to_dict() for item in renewer_infos_all]
        print(data)
        return render_template('review.html', results=data)
    


    

@app.route('/calendar_time')
def get_calendar_time():
    gap_day_remind_datetime = datetime.strptime(gap_day_remind, '%Y/%m/%d')
    data = {
        "gap_day_remind": gap_day_remind_datetime, 
        "next_gap_day_return": next_gap_day_return
    }
    return jsonify(data)











#以下為審核路由

@app.route('/accept-user', methods=['POST'])
def accept_update_viewed_status():
    data = request.json  # 假設前端以 JSON 格式發送數據
    data_type = data.get('dataType')
    tag = data.get('Tag')
    DiscordUsername = data.get('DiscordUsername')
    _, end_time_get_info = compare_time(gap_day_remind, next_gap_day_return)
    print(data)
    if data_type == 'streamer':
        streamer_info = StreamerInfo.query.filter_by(Tag=tag).first()
        if streamer_info:
            streamer_info.Viewed = 'yes'  # 更新 Viewed 屬性
            db.session.commit()  # 提交變更到數據庫

            member_info_new_from_web = MemberInfo(
            DiscordUsername=streamer_info.DiscordUsername,
            DiscordUserID=None,  # 傳遞null值
            MinecraftName=streamer_info.MinecraftName,
            Position=streamer_info.Position,
            PassTime=end_time_get_info,  # 傳遞null值
            Email=streamer_info.Email
        )
            db.session.add(member_info_new_from_web)
            db.session.commit()  # 提交變更到數據庫
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "StreamerInfo updated successfully"}), 200
        else:
            return jsonify({"message": "StreamerInfo not found"}), 404
    elif data_type == 'wingman':
        wingman_info = WingmanInfo.query.filter_by(Tag=tag).first()
        if wingman_info:
            wingman_info.Viewed = 'yes'
            db.session.commit()

            member_info_new_from_web = MemberInfo(
            DiscordUsername=wingman_info.DiscordUsername,
            DiscordUserID=None,  # 傳遞null值
            MinecraftName=wingman_info.MinecraftName,
            Position=wingman_info.Position,
            PassTime=end_time_get_info,  # 傳遞null值
            Email=wingman_info.Email
        )
            db.session.add(member_info_new_from_web)
            db.session.commit()  # 提交變更到數據庫
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "WingmanInfo updated successfully"}), 200
        else:
            return jsonify({"message": "WingmanInfo not found"}), 404
    elif data_type == 'renewer':
        renewer_info = RenewerInfo.query.filter_by(Tag=tag).first()
        if renewer_info:
            renewer_info.Viewed = 'yes'
            db.session.commit()

            member_info_new_from_web = MemberInfo(
            DiscordUsername=renewer_info.DiscordUsername,
            DiscordUserID=None,  # 傳遞null值
            MinecraftName=renewer_info.MinecraftName,
            Position=renewer_info.Position,
            PassTime=end_time_get_info,  # 傳遞null值
            Email=renewer_info.Email
        )
            db.session.add(member_info_new_from_web)
            db.session.commit()  # 提交變更到數據庫
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "RenewerInfo updated successfully"}), 200
        else:
            return jsonify({"message": "RenewerInfo not found"}), 404



@app.route('/deny-user', methods=['POST'])
def deny_update_viewed_status():
    data = request.json  
    print(data)
    data_type = data.get('dataType')
    tag = data.get('Tag')
    DiscordUsername = data.get('DiscordUsername')

    if data_type == 'streamer':
        streamer_info = StreamerInfo.query.filter_by(Tag=tag).first()
        if streamer_info:
            streamer_info.Viewed = 'yes'  # 更新 Viewed 屬性
            db.session.commit()  # 提交變更到數據庫
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "StreamerInfo updated successfully"}), 200
        else:
            return jsonify({"message": "StreamerInfo not found"}), 404
    elif data_type == 'wingman':
        wingman_info = WingmanInfo.query.filter_by(Tag=tag).first()
        if wingman_info:
            wingman_info.Viewed = 'yes'
            db.session.commit()
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "WingmanInfo updated successfully"}), 200
        else:
            return jsonify({"message": "WingmanInfo not found"}), 404
    elif data_type == 'renewer':
        renewer_info = RenewerInfo.query.filter_by(Tag=tag).first()
        if renewer_info:
            renewer_info.Viewed = 'yes'
            db.session.commit()
            change_all_form_viewed_by_discordusername(DiscordUsername)
            return jsonify({"message": "RenewerInfo updated successfully"}), 200
        else:
            return jsonify({"message": "RenewerInfo not found"}), 404


def change_all_form_viewed_by_discordusername(name):
    if name:
        StreamerInfo.query.filter_by(DiscordUsername=name).update({'Viewed': 'yes'})
        
        # 更新WingmanInfo
        WingmanInfo.query.filter_by(DiscordUsername=name).update({'Viewed': 'yes'})
        
        # 更新RenewerInfo
        RenewerInfo.query.filter_by(DiscordUsername=name).update({'Viewed': 'yes'})
        
        db.session.commit()  # 提交所有變更
        return jsonify({"message": "All related forms have been updated"}), 200
    else:
        return jsonify({"message": "DiscordUsername is required"}), 400



##往上審核路由







@app.route('/show-member')
@login_required
def show_members():
    if current_user.role not in ['manager', 'superadmin']:
        return render_template('no_permission.html')
    members = MemberInfo.query.all()
    return render_template('members.html', members=members)

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    member_to_delete = MemberInfo.query.get_or_404(member_id)
    db.session.delete(member_to_delete)
    db.session.commit()
    return redirect(url_for('show_members'))

@app.route('/show-member-discord')
def show_members_discord():
    members = MemberInfo.query.with_entities(
        MemberInfo.DiscordUsername, 
        MemberInfo.DiscordUserID, 
        MemberInfo.MinecraftName, 
        MemberInfo.Position, 
        MemberInfo.PassTime
    ).all()

    # 將查詢結果轉換為字典列表
    members_list = [
        {
            'DiscordUsername': member.DiscordUsername, 
            'DiscordUserID': member.DiscordUserID, 
            'MinecraftName': member.MinecraftName, 
            'Position': member.Position, 
            'PassTime': member.PassTime
        } 
        for member in members
    ]

    # 使用 jsonify 返回JSON響應
    return jsonify(members_list)




def delete_expired_members(cutoff_date_str):
    cutoff_date_str = str(cutoff_date_str)
    cutoff_date = datetime.strptime(cutoff_date_str , "%Y-%m-%d %H:%M:%S")
    print(cutoff_date)
    # 查詢所有PassTime不是'permanent'且小於cutoff_date的成員
    expired_members = MemberInfo.query.filter(
        MemberInfo.PassTime != 'permanent'
    ).filter(
        MemberInfo.PassTime < cutoff_date
    ).all()
    
    for member in expired_members:
        db.session.delete(member)
        print(cutoff_date,"1")
    
    # 提交更改到數據庫
    db.session.commit()




##時間處理區

def tick():
    real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    socketio.emit('update_time', {'time': real_time})


def run_time_management_loop(start_date_str, year):
    global current_date_str, gap_day_remind, end_date_year_loop, strat_date_return, next_gap_day_return, next_end_day_return
    current_date_str, gap_day_remind, end_date_year_loop, strat_date_return, next_gap_day_return, next_end_day_return = time_cal.time_management_system(start_date_str, year)
    while True:
        current_date = datetime.strptime(current_date_str, '%Y/%m/%d')
        #print(current_date)
        now = datetime.now()
        #print(current_date_str, gap_day_remind, end_date_year_loop, strat_date_return, next_gap_day_return, next_end_day_return)
        tick()
    
        if now >= next_gap_day_return:
            print(f"達到終止日: {next_end_day_return}，正在重新計算...")
            current_date_str, gap_day_remind, end_date_year_loop, strat_date_return, next_gap_day_return, next_end_day_return = time_cal.time_management_system(current_date_str.split('/')[1] + "/" + current_date_str.split('/')[2], end_date_year_loop)
            print(f"新的終止日是: {next_end_day_return}")
            with app.app_context():
                delete_expired_members(strat_date_return)
        time.sleep(1)  

def start_time_management_thread(start_date_str, year):
    thread = threading.Thread(target=run_time_management_loop, args=(start_date_str, year))
    thread.daemon = True
    thread.start()

##時間處理區


##discord專屬路由
@app.route('/form-count-discord-bot')
def get_info_count():
    # 假設 get_info() 是上面提供的函數，它返回包含 streamers、wingmans 和 renewers 資料的字典
    data = get_info().get_json()  # 假設 get_info() 能夠以某種方式被直接調用並返回JSON資料
    
    # 計算每個類別中的資料筆數
    total_count = sum(len(data[category]) for category in ['streamers', 'wingmans', 'renewers'])
    print(total_count)
    # 返回總筆數
    return jsonify({"total_count": total_count})


def query_join_user_discord_Memberusername(discordusername):
    Member_query = MemberInfo.query.filter_by(DiscordUsername=discordusername).all()
    return Member_query
def query_join_user_discord_info(discordusername):
    streamer_join_user_discord_infos = StreamerInfo.query.filter_by(DiscordUsername=discordusername).with_entities(StreamerInfo.SubmitTime,StreamerInfo.Viewed).all()
    wingman_join_user_discord_infos = WingmanInfo.query.filter_by(DiscordUsername=discordusername).with_entities(WingmanInfo.SubmitTime,WingmanInfo.Viewed).all()
    renewer_join_user_discord_infos = RenewerInfo.query.filter_by(DiscordUsername=discordusername).with_entities(RenewerInfo.SubmitTime,RenewerInfo.Viewed).all()
    return streamer_join_user_discord_infos, wingman_join_user_discord_infos, renewer_join_user_discord_infos



@app.route('/check-join-user-state', methods=["GET"])
def check_join_user_state():
    discordusername = request.args.get('discordusername')
    print(query_join_user_discord_info(discordusername))
    if not discordusername:
        return jsonify({"error": "Tag parameter is required"}), 400
    else:
        s_form, w_form, r_form =query_join_user_discord_info(discordusername)
        check_permission = query_join_user_discord_Memberusername(discordusername)
        if check_permission:
            return jsonify("1")
        elif (find_join_user_form_state(s_form) == "no_form_in_db_this_period" and
            find_join_user_form_state(w_form) == "no_form_in_db_this_period" and
            find_join_user_form_state(r_form) == "no_form_in_db_this_period"):
                return jsonify("2")
        elif (find_join_user_form_state(s_form) == "form_review_not_done_yet" or 
            find_join_user_form_state(w_form) == "form_review_not_done_yet" or 
            find_join_user_form_state(r_form) == "form_review_not_done_yet"):
                return jsonify("3")
        else:
            return jsonify("4")

def find_join_user_form_state(results):
    start_time_get_info, end_time_get_info = compare_time(gap_day_remind, next_gap_day_return)
    utc_zone = pytz.utc
    taiwan_zone = pytz.timezone('Asia/Taipei')
    count_review_done = 0
    count_review_not_done_yet = 0
    for item in results:
        tran_submit_time_to_compare = datetime.fromisoformat(item[0].replace('Z', '+00:00')).replace(tzinfo=utc_zone)
        tran_submit_time_to_compare_taiwan = tran_submit_time_to_compare.astimezone(taiwan_zone)
        tran_submit_time_to_compare_naive = tran_submit_time_to_compare_taiwan.replace(tzinfo=None)  # 移除時區資訊
        test_Viewed = item[1]
        if start_time_get_info < tran_submit_time_to_compare_naive < end_time_get_info and test_Viewed == "no":
            count_review_not_done_yet += 1
        elif start_time_get_info < tran_submit_time_to_compare_naive < end_time_get_info and test_Viewed == "yes":
            count_review_done += 1
    if count_review_not_done_yet == 0 and count_review_done == 0:
        return("no_form_in_db_this_period")
    if count_review_not_done_yet > 0:
        return("form_review_not_done_yet")



@app.route('/query_discord_embed_card', methods=['GET'])
def query_discord_embed_card():
    discord_username = request.args.get('discord_username')
    viewed_state = "no"
    data = []

    # 從StreamerInfo表中查詢
    streamer_results = StreamerInfo.query.filter_by(DiscordUsername=discord_username, Viewed=viewed_state).all()
    print(streamer_results)
    for result in streamer_results:
        data.append({
            'Type': 'StreamerInfo',
            'DiscordUsername': result.DiscordUsername,
            'MinecraftName': result.MinecraftName,
            'Email': result.Email,
            'Duration': result.Duration,
            'Position': result.Position,
            'Nickname': result.Nickname,
            'ChannelUrl': result.ChannelUrl,
            'Works': result.Works,
            'Motivation': result.Motivation,
            'DesiredMember': result.DesiredMember,
            'PostApprovalActivity': result.PostApprovalActivity,
            'SelfIntroduction': result.SelfIntroduction,
            'SubmitTime': result.SubmitTime,
            'Tag': result.Tag,
            'Viewed': result.Viewed,
            'dataType': 'streamer'
        })

    # 從WingmanInfo表中查詢
    wingman_results = WingmanInfo.query.filter_by(DiscordUsername=discord_username).all()
    for result in wingman_results:
        data.append({
            'Type': 'WingmanInfo',
            'DiscordUsername': result.DiscordUsername,
            'MinecraftName': result.MinecraftName,
            'Email': result.Email,
            'Duration': result.Duration,
            'Position': result.Position,
            'Nickname': result.Nickname,
            'Motivation': result.Motivation,
            'ClosestMember': result.ClosestMember,
            'MemberDuration': result.MemberDuration,
            'SelfIntroduction': result.SelfIntroduction,
            'SubmitTime': result.SubmitTime,
            'Tag': result.Tag,
            'Viewed': result.Viewed,
            'dataType': 'wingman'
        })

    # 從RenewerInfo表中查詢
    renewer_results = RenewerInfo.query.filter_by(DiscordUsername=discord_username).all()
    for result in renewer_results:
        data.append({
            'Type': 'RenewerInfo',
            'DiscordUsername': result.DiscordUsername,
            'MinecraftName': result.MinecraftName,
            'Email': result.Email,
            'Duration': result.Duration,
            'Position': result.Position,
            'Renewer_nickname': result.Renewer_nickname,
            'SubmitTime': result.SubmitTime,
            'Tag': result.Tag,
            'Viewed': result.Viewed,
            'dataType': 'renewer'
        })

    if data:
        return jsonify(data)
    else:
        return jsonify({'message': 'No data found for the given Discord username.'}), 404






@app.route('/update_discord_user_id', methods=['POST'])
def update_discord_user_id():
    data = request.json  # 從前端獲取JSON資料
    discord_username = data.get('discordusername')  # 從JSON資料中獲取discordusername
    new_discord_user_id = data.get('discorduserid')  # 從JSON資料中獲取新的discorduserid

    # 查找匹配的MemberInfo紀錄
    member_info = MemberInfo.query.filter_by(DiscordUsername=discord_username).first()
    if member_info:
        member_info.DiscordUserID = new_discord_user_id  # 更新DiscordUserID
        db.session.commit()  # 提交變更到資料庫
        return jsonify({"message": "User ID updated successfully."}), 200
    else:
        return jsonify({"error": "Member not found."}), 404













#啟動初始設定
def insert_member_info_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for item in data:
        if not MemberInfo.query.filter_by(DiscordUserID=item['discord_id']).first():
            new_member = MemberInfo(
                DiscordUsername=item['discord_username'],
                DiscordUserID=item['discord_id'],
                MinecraftName=item['minecraft_username'],
                Position=item['position'],
                PassTime=item['passtime'],
                Email=item['email'] if item['email'] != 'null' else None
            )
            db.session.add(new_member)
    db.session.commit()






start = "1/28"
current_year = datetime.now().year
start_year = current_year


if __name__ == '__main__':
    start_time_management_thread(start, start_year)
    with app.app_context():
        db.create_all()  # 創建數據庫表 
        create_superadmin()  # 創建超級管理員用戶
        insert_member_info_from_json('C:/Users/User/Desktop/management_system/backend/json/fixed-member.json')
    socketio.run(app, debug=True, host='localhost', port=25566) #感謝我們的flask，如果開debug，thread會執行兩次，祖刻薄:6
