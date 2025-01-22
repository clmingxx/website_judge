from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify


app = Flask(__name__, static_folder = 'static')
app.secret_key = 'your_secret_key'  # 用于会话管理


# 模拟的用户数据库
from vars import *


@app.route('/')
def home():
    # if 'username' in session:
    #     return f'Welcome, {session["username"]}! <br><a href="/logout">Logout</a>'
    generate_qrcode(f"http://{get_local_ip()}:5000/login", "qrcode.png")
    return render_template('home.html')


@app.route('/admin')
def admin():
    if 'username' not in session or session['username'] != 'admin':
        session.clear()
        flash('非管理员用户')
        return redirect(url_for('login'))
    return render_template('admin.html', users=users, items=items, scores=scores)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admins and passwords[username] == password:
            session['username'] = username
            if session['username'] == 'admin':
                return redirect(url_for('admin'))
        if username in users and passwords[username] == password:
            session['username'] = username
            return redirect(url_for('judge'))
        else:
            flash('无效的用户名或密码')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/judge')
def judge():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_scores = scores[username]
    return render_template('judge.html', username=username, items=items, user_scores=user_scores)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    if 'username' not in session:
        return jsonify({'success': False, 'message': '未登录用户'})

    username = session['username']
    item = request.form['item']
    score = int(request.form['score'])

    scores[username][item] = score
    # print(scores)
    return jsonify({'success': True, 'message': '打分成功'})


@app.route('/display')
def display():
    # 计算每个项目的总成绩
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

    # 按总成绩排序
    results.sort(key=lambda x: x['total_score'] if isinstance(x['total_score'], float) else -1, reverse=True)
    return render_template('display.html', results=results)


@app.route('/display/<item_name>')
def display_item(item_name):
    item_details = None
    for item in items:
        if item == item_name:
            scores_list = [scores[user][item] for user in users if scores[user][item] is not None]
            if len(scores_list) == len(users):  # 所有用户都已评分
                total_score = sum(scores_list) / len(scores_list)
                highest_score = max(scores_list)
                lowest_score = min(scores_list)

                # 找到最高分和最低分的用户
                highest_score_user = next(user for user in users if scores[user][item] == highest_score)
                lowest_score_user = next(user for user in users if scores[user][item] == lowest_score)

                item_details = {
                    'item': item,
                    'total_score': round(total_score, 2),
                    'scores': {user: scores[user][item] for user in users},
                    'highest_score': highest_score,
                    'highest_score_user': highest_score_user,
                    'lowest_score': lowest_score,
                    'lowest_score_user': lowest_score_user
                }
            else:
                item_details = {
                    'item': item,
                    'total_score': '评分未完成',
                    'scores': {user: scores[user][item] for user in users}
                }
            break

    if item_details:
        return render_template('item_details.html', item_details=item_details)
    else:
        return "项目未找到", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')