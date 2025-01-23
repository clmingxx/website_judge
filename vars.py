import os
import random
import socket
import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask,SquareGradiantColorMask
passwords = {
    'admin': 'admin',
    'user1': 'user1',
    'user2': 'user2'
}
admins = ['admin']
users = [
    'user1', 'user2', '张三', '李四', '王五', '赵六', 'user7', 'user8', 'user9', 'user10',
    'user11', 'user12', '钱七', '孙八', '周九', '吴十', 'user16', 'user17', 'user18', 'user19',
    'user20', 'user21', '郑十一', '王十二', '冯十三', '陈十四', 'user26', 'user27', 'user28', 'user29',
    'user30', 'user31', '沈十五', '韩十六', '杨十七', '徐十八', 'user36', 'user37', 'user38', 'user39',
    'user40', 'user41', '高十九', '朱二十', '秦二十一', '尤二十二', 'user46', 'user47', 'user48', 'user49',
    'user50'
]
# users = [
#     'user1', 'user2', '张三'
# ]
items = ['立足“后亚运”奋进“双一流”，努力探索城市核心区派出所主防工作最佳实践主防工作最佳实践主防工作最佳实践', '全力促主防，系好安全“戴', '项目3', '项目4', '项目5', '项目6', '项目7', '项目8', '项目9', '项目10', '项目11']
scores = {user: {item: None for item in items} for user in users}
# 测试用的 speakers 字典
speakers = {
    '立足“后亚运”奋进“双一流”，努力探索城市核心区派出所主防工作最佳实践主防工作最佳实践主防工作最佳实践': {'name': '杭州市公安局'},
    '全力促主防，系好安全“戴': {'name': '萧山分局'},
    '项目3': {'name': '科通科'},
    '项目4': {'name': '发言人D'},
    '项目5': {'name': '发言人E'},
    '项目6': {'name': '发言人F'},
    '项目7': {'name': '发言人G'},
    '项目8': {'name': '发言人H'},
    '项目9': {'name': '发言人I'},
    '项目10': {'name': '发言人J'},
    '项目11': {'name': '发言人K'}
}
for user in users:
    for item in items:
        if user is not 'user1':
            scores[user][item] = random.randint(0, 100)
def get_local_ip():
    # 获取本地 IP 地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

def generate_qrcode(url, filename="static/images/qrcode.png"):
    # 生成二维码并保存到指定路径
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    # img = qr.make_image(image_factory=StyledPilImage, color_mask=SquareGradiantColorMask(), embeded_image_path="static/images/xcloud.jpg")
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join('static\\images\\', filename))
    # img.save(filename)
    print('save qrcode')
if __name__ == '__main__':
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    qrcode_path = "qrcode.png"
    generate_qrcode(url, qrcode_path)