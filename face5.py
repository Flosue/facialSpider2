# -*- coding: utf-8 -*-
#  识别图片中的所有人脸并显示出来
# filename : find_faces_in_picture.py


# 导入pil模块 ，可用命令安装 apt-get install python-Imaging
from PIL import Image
# 导入face_recogntion模块，可用命令安装 pip install face_recognition
import face_recognition
import os
import number
import savemysql

def faceClasify(Root1,num):
    # 将jpg文件加载到numpy 数组中
    theRoot=Root1+num+'.jpg'
    image = face_recognition.load_image_file(theRoot)
    face_locations = face_recognition.face_locations(image)
    # 打印：我从图片中找到了 多少 张人脸
    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    if len(face_locations)==0:
        print("没有人脸")
        return 0

    #判断是否有主角
    #主角人脸
    picture_of_main = face_recognition.load_image_file("E:\project\sample.jpg")
    main_face_encoding = face_recognition.face_encodings(picture_of_main)[0]
    #待检测人脸
    unknown_picture = face_recognition.load_image_file(theRoot)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    results = face_recognition.compare_faces([unknown_face_encoding], main_face_encoding)
    if results[0] == False:
        print("没有主角")
        return -1

    i=0#脸的次数

    # 循环找到的所有人脸
    for face_location in face_locations:
        # 打印每张脸的位置信息
        i+=1
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        # 指定人脸的位置信息，然后显示人脸图片
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        print("1")
        #print("e:/project/allface/%s_%s.jpg" % num, str(i))
        #with open('e:/project/1/%d.jpg' % i, 'wb')as f:
        #f.write(pil_image.content)
        #    f.write(pil_image.content)
        pil_image.save(r'e:/project/allface/%s_%s.jpg' % (num, str(i)))
        #pil_image.save('e:/project/1/' + str(face_location) + '.png')
        #pil_image.show()
        print("2")
        pil_picture = face_recognition.load_image_file(r'e:/project/allface/%s_%s.jpg' % (num, str(i)))
        print("3")
        try:
            prepeo_face_encoding = face_recognition.face_encodings(pil_picture)[0]
        except Exception as e:
            print("未能识别出人脸")
            continue
        print("4")
        result1=face_recognition.compare_faces([prepeo_face_encoding], main_face_encoding)
        if result1[0] == True:
            print("peosamemain")
            continue

        #判断是否在已有人群中
        flag=0#判断是否有相似
        for peo in range(0,number.COUNT_FACE):
            print("peo")
            picture_of_peo = face_recognition.load_image_file(r"E:\project\allpeo\%s.jpg" % str(peo+1))
            peo_face_encoding = face_recognition.face_encodings(picture_of_peo)[0]

            result2 = face_recognition.compare_faces([prepeo_face_encoding], peo_face_encoding)
            if result2[0] ==True:
                print("peosameface")
                number.FACE_NUM[peo]+=1
                flag=1
                break
        if flag==0:
            print("peoadd")
            number.COUNT_FACE+=1
            number.FACE_NUM.append(1)
            pil_image.save(r'e:/project/allpeo/%s.jpg' % str(number.COUNT_FACE))
            print(number.COUNT_FACE)


    return len(face_locations)