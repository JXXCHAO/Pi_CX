import cv2
import time
import os
from threading import Thread
from toEmail import toEmail
from bypy import ByPy

def war_ing(path):
    my_sender = 'xxxx'           # 发件人邮箱账号
    my_pass = 'xxx'              # 发件人邮箱密码
    my_user = 'jxxchao@qq.com'   # 收件人邮箱账号
    while(True):
        time.sleep(30)           # 30s为一周期
        filelist = os.listdir('../image')                   # 图片文件保存路径 无则需要新建 绝对路径 相对路径均可
        if len(filelist) != 0:
            print('开始将文件备份至云端')
            besync(path)                                    # 同步图片文件至百度云盘
            print('将文件备份至云端已完成')
            toE = toEmail(my_sender, my_pass, [my_user, ])  # 发送邮件封装的类 创建并初始化
            print('发送报警邮件')
            toE.sendEmail("../image")                       # 制定 图片文件的路径 并发送报警邮件
            if toE.getFlag:                                 # 判断 邮件是否发送成功
                print('邮件发送成功')
            else:
                print('邮件发送失败')

            for file in os.listdir(path):                   # 该操作为遍历文件夹 删除文件 不需要在本地存放
                if os.path.isdir(file):
                    continue
                else:
                    filename = os.path.join(path, file)     # 文件绝对路径
                    os.remove(filename)


def besync(path):                                           # 云盘同步函数 可能因hash导致显示失败，但实际成功。
    dir_name = '监控扩展数据'
    pan = ByPy()
    pan.mkdir(dir_name)
    for file in os.listdir(path):
        if os.path.isdir(file):                             # 判断 是文件夹跳过
            continue
        else:
            filename = os.path.join(path, file)             # 文件绝对路径
            pan.upload(localpath=filename, remotepath=dir_name, ondup='newcopy')    # 上传图片

def be_work():
    cap = cv2.VideoCapture(0) # 使用摄像头
    face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')  # 加载人脸特征库
    count = 0
    time_1 = time.strftime("../image/%Y%m%d%H%M%S", time.localtime())   # 时间1
    while(True):
        ret, frame = cap.read() # 读取一帧的图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 转灰

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5))   # 检测人脸
        facenum = len(faces)
        print(facenum)
        time_n = time.strftime("../image/%Y%m%d%H%M%S", time.localtime())  # 时间2
        if facenum != 0 and time_n != time_1 and facenum - count > 0:      # 当发现有人 且 不再同一秒 且  人 数发生了变化  取一帧保留
            filename = time_n + '.jpg'                                     # 保存文件命名
            print("发现{0}个人脸!".format(len(faces)))
            print(filename)
            print(cv2.imwrite(filename, frame))                            # 保存图像文件
        count = facenum

        for(x, y, w, h) in faces:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)    # 用矩形圈出人脸
        cv2.imshow('Face Recognition', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):                              # 跳出循环
            break
    cap.release() # 释放摄像头
    cv2.destroyAllWindows()



if __name__ == '__main__':
    try:
        thread_01 = Thread(target=be_work)                          # 创建工作线程 --  监控
        thread_02 = Thread(target=war_ing, args=('../image', ))     # 报警 -  数据同步
        thread_01.start()                                           # 启动线程1
        thread_02.start()                                           # 启动线程2
        while True:                                                 # 可替换为  thread_01.join()  thread_02.join()
            pass
    except:
        print("Error: 无法启动线程")
