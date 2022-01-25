#!/usr/bin/env python
# coding=utf-8

import os
import shutil
from flask import Flask, request, Response,redirect, render_template as rt
app = Flask(__name__)


saveDir = './upload/'
# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
@app.route('/',defaults={'fileName': None}, methods=['GET'])
@app.route('/<path:fileName>', methods=['GET'])
def index(fileName):
    print("fileName is ",fileName)
    global saveDir
    url = request.args.get('url', None)
    print("url is ",url)
    print("saveDir is ",saveDir)
    print("changeDir is ",changeDir)
    if url != None and changeDir:
        if os.path.isdir(url):
            saveDir = str(url)
            print("saveDir is ",saveDir)
            redirect('/')
    if fileName == None:
        files = os.listdir(saveDir)  # 获取文件目录
        return rt('./index.html', files=files, saveDir = saveDir)
# def file_download(fileName):
    print("fileName is ",fileName)
    # print(os.path.isdir(fileName))
    if os.path.isdir(saveDir + fileName):
        if fileName[-1] != '/':
            return redirect('/'+fileName + '/')
        print("fileName is ",fileName)
        files = os.listdir(saveDir+fileName)
        print("files is ",files)
        return rt('./index.html', files = files, saveDir = saveDir+fileName)
    if not os.path.exists(saveDir + fileName):
        return "file not exists"
    def send_chunk():  # 流式读取
        store_path = saveDir + '%s' % fileName
        print("store is ",store_path)
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk
    return Response(send_chunk(), content_type='application/octet-stream')

# @app.route('/',defaults={'fileName': None}, methods=['POST'])
# @app.route('/<path:fileName>', methods=['POST'])
# def upload_part(fileName):  # 接收前端上传的一个分片
#     saveDirN = saveDir
#     print("fileName is ",fileName)
#     if fileName != None:
#         saveDirN = saveDir + '/' + fileName + '/'
#     saveName = request.form.get('name')  # 获取文件的唯一标识符
#     chunks = request.form.get('chunks')  # 获取该分片在所有分片中的序号
#     chunk = request.form.get('chunk')  # 获取该分片在所有分片中的序号
#     if chunks != None:
#         saveName = '%s_%s' % (saveName, chunk)  # 构造该分片的唯一标识符
#         # saveName = request.form.get('name')  # 获取文件的唯一标识符
#     upload_file = request.files['file']
#     upload_file.save(saveDirN + '%s' % saveName)  # 保存分片到本地
#     print("upload ",(saveDirN + '%s' % saveName))
#     if chunks == None: return 'success'
#     # print("upload_file is \n\n\n",upload_file)
#     # fout = open(('./upload/%s' % saveName),'ab')
#     # fout.write(upload_file)
#     # fout.close()
#     # return 1
#     # upload_file.save('./upload/%s' % saveName)  # 保存分片到本地
#     if int(chunk) == (int(chunks)-1):
#         target_fileName = request.form.get('name')  # 获取上传文件的文件名
#         # task = request.args.get('task_id')  # 获取文件的唯一标识符
#         chunk = 0  # 分片序号
#         with open(saveDirN + '%s' % target_fileName, 'wb') as target_file:  # 创建新文件
#             while True:
#                 try:
#                     fileName = saveDirN + '%s_%s' % (target_fileName, chunk)
#                     source_file = open(fileName, 'rb')  # 按序打开每个分片
#                     target_file.write(source_file.read())  # 读取分片内容写入新文件
#                     source_file.close()
#                 except Exception as e:
#                     # print("error is ",e)
#                     break
#                 chunk += 1
#                 os.remove(fileName)  # 删除该分片，节约空间
#         print("upload all chunks saveas ",target_fileName)
#     return str(0)
#     # return rt('./index.html')

@app.route('/',defaults={'fileName': None}, methods=['POST'])
@app.route('/<path:fileName>', methods=['POST'])
def upload_part(fileName):  # 接收前端上传的一个分片
    # print("request.form is \n",request.form)
    nowDirN = saveDir
    # print("fileName is ",fileName)
    if fileName != None:
        nowDirN = saveDir + '/' + fileName + '/'
    saveName = request.form.get('name')  # 获取文件的唯一标识符
    chunks = request.form.get('chunks')  # 获取该分片在所有分片中的序号
    chunk = request.form.get('chunk')  # 获取该分片在所有分片中的序号
    try:os.mkdir((nowDirN+saveName+'.Save'),755)
    except Exception as e:print(e)
    saveDirN = nowDirN + (saveName+'.Save' + '/') 
    if chunks != None:
        saveName = '%s_%s' % (saveName, chunk)  # 构造该分片的唯一标识符  
        os.rmdir(saveDirN)
        saveDirN = nowDirN
        # saveName = request.form.get('name')  # 获取文件的唯一标识符
    upload_file = request.files['file']
    upload_file.save(saveDirN + '%s' % saveName)  # 保存分片到本地
    print("upload ",(saveDirN + '%s' % saveName))
    if chunks == None: return 'success'
    # print("upload_file is \n\n\n",upload_file)
    # fout = open(('./upload/%s' % saveName),'ab')
    # fout.write(upload_file)
    # fout.close()
    # return 1
    # upload_file.save('./upload/%s' % saveName)  # 保存分片到本地
    target_fileName = request.form.get('name')  # 获取上传文件的文件名
    # task = request.args.get('task_id')  # 获取文件的唯一标识符
    # chunk = 0  # 分片序号
    # print((os.listdir(saveDirN)))
    # print(len(os.listdir(saveDirN)))
    # print(chunks)
    # print(len(os.listdir(saveDirN)) == chunks)
    if len(os.listdir(saveDirN)) == int(chunks):
        print("All file chunks got ",saveDirN + '%s' % target_fileName)
        chunk = 0
        with open(saveDirN + '%s' % target_fileName, 'wb') as target_file:  # 创建新文件
            while True:
                try:
                    fileName = saveDirN + '%s_%s' % (target_fileName, chunk)
                    source_file = open(fileName, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                    os.remove(fileName)  # 删除该分片，节约空间
                except Exception as e:
                    print("error is ",e)
                    break
                chunk += 1
        shutil.move(saveDirN+target_fileName,nowDirN+target_fileName)
        os.rmdir(saveDirN)
        print("upload all chunks save as ",target_fileName)
        return str(1)
    else:
        return str(0)
    # return rt('./index.html')

import sys

changeDir = False
def mainApp():
    print("Usage py server.py saveDir ifCanChangeDir port")
    host = '0.0.0.0'
    port = '8765'
    debugT = False
    print(sys.argv)
    try:
        global changeDir 
        global saveDir
        saveDir = sys.argv[1]
        changeDir = sys.argv[2]
        port = sys.argv[3]
    except Exception as e:
        pass
    print('saveDir is :\n',saveDir,'\nIf or not can change dir:\n',changeDir,'\n')
    app.run(host=host,port=port,debug = debugT)

if __name__ == '__main__':
    mainApp()