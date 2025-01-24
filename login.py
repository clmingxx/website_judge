from os import urandom
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps

app = Flask(__name__, static_folder='static')
app.secret_key = urandom(16)  # 用于会话管理

# 模拟的用户数据库
from vars import *

# 装饰器：登录验证
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录！', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 装饰器：管理员权限验证
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] != 'admin':
            flash('非管理员用户', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    generate_qrcode(f"http://{get_local_ip()}:5000/login", "qrcode.png")
    return render_template('home.html')


@app.route('/admin')
@admin_required  # 使用管理员权限验证装饰器
def admin():
    return render_template('admin.html', users=users, items=items, scores=scores)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:  # 如果用户已经登录
        flash('您已经登录！', 'info')
        return redirect(url_for('judge'))  # 跳转到用户页面

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admins and passwords[username] == password:
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('admin'))
        elif username in users and passwords[username] == password:
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('judge'))
        else:
            flash('无效的用户名或密码', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        flash('您已登出！', 'success')
        session.pop('username', None)
    else:
        session.clear()
        flash('您尚未登录！', 'warning')
    return redirect(url_for('login'))


@app.route('/judge')
@login_required  # 使用登录验证装饰器
def judge():
    username = session['username']
    user_scores = scores[username]
    return render_template('judge.html', username=username, items=items, user_scores=user_scores)


@app.route('/submit_score', methods=['POST'])
@login_required  # 使用登录验证装饰器
def submit_score():
    username = session['username']
    item = request.form['item']
    score = int(request.form['score'])

    scores[username][item] = score
    return jsonify({'success': True, 'message': '打分成功'})


@app.route('/display')
@login_required  # 使用登录验证装饰器
def display():
    results = []
    for item in items:
        scores_list = [scores[user][item] for user in users if scores[user][item] is not None]
        if len(scores_list) == len(users):  # 所有用户都已评分
            if len(scores_list) <= 2:
                total_score = sum(scores_list) / len(scores_list)
            else:
                scores_list.remove(max(scores_list))
                scores_list.remove(min(scores_list))
                total_score = sum(scores_list) / len(scores_list)
            results.append({
                'item': item,
                'total_score': round(total_score, 2),
                'scores': {user: scores[user][item] for user in users},
                'highest_score': max(scores_list),
                'lowest_score': min(scores_list),
                'speaker': speakers[item]['name']  # 只传递发言人名字
            })
        else:
            results.append({
                'item': item,
                'total_score': '评分未完成',
                'scores': {user: scores[user][item] for user in users},
                'speaker': speakers[item]['name']  # 只传递发言人名字
            })

    results.sort(key=lambda x: x['total_score'] if isinstance(x['total_score'], float) else -1, reverse=True)
    return render_template('display.html', results=results)


@app.route('/display/<item_name>')
@login_required  # 使用登录验证装饰器
def display_item(item_name):
    item_details = None
    for item in items:
        if item == item_name:
            scores_list = [scores[user][item] for user in users if scores[user][item] is not None]
            num_users = len(users)
            num_scored = len(scores_list)
            num_unscored = num_users - num_scored

            item_details = {
                'item': item,
                'num_users': num_users,
                'num_unscored': num_unscored,
                'scores_list': scores_list,
                'highest_score_index': None,
                'lowest_score_index': None,
                'total_score': None
            }

            if num_scored > 1:  # 至少有2个评委打分
                highest_score = max(scores_list)
                lowest_score = min(scores_list)
                highest_score_index = scores_list.index(highest_score)
                lowest_score_index = scores_list.index(lowest_score)

                item_details.update({
                    'highest_score': highest_score,
                    'highest_score_index': highest_score_index,
                    'lowest_score': lowest_score,
                    'lowest_score_index': lowest_score_index
                })

                if num_scored == num_users:  # 所有评委都已评分
                    if num_users <= 2:
                        total_score = sum(scores_list) / num_users
                    else:
                        sorted_scores = sorted(scores_list)
                        trimmed_scores = sorted_scores[1:-1]
                        total_score = sum(trimmed_scores) / len(trimmed_scores)
                    item_details['total_score'] = round(total_score, 2)
                else:
                    item_details['total_score'] = f'评分未完成（{num_unscored}位评委未打分）'
            else:
                item_details['total_score'] = '暂无评分'
            break

    if item_details:
        return render_template('item_details.html', item_details=item_details)
    else:
        return "项目未找到", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')