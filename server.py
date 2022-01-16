#!/usr/bin/env python
# coding=utf-8

import os
from flask import Flask, request, Response,Blueprint, render_template as rt
bp = Blueprint('bp', __name__, template_folder='templates')
app = Flask(__name__)
# app.register_blueprint(bp)
# def create_app():
#     app = Flask(__name__)
#     # existing code omitted
#     # from . import auth
#     app.register_blueprint(auth.bp)
#     return app

# app = create_app()

saveDir = './upload/'
# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
@app.route('/',defaults={'filename': None}, methods=['GET'])
@app.route('/<path:filename>', methods=['GET'])
def index(filename):
    print("filename is ",filename)
    if filename == None:
        files = os.listdir(saveDir)  # 获取文件目录
        return rt('./index.html', files=files)

# def file_download(filename):
    print("filename is ",filename)
    print(os.path.isdir(filename))
    if os.path.isdir(saveDir + filename):
        print("filename is ",filename)
        files = os.listdir(saveDir+filename)
        print("files is ",files)
        return rt('./index.html', files=files,baseUrl = filename)
    def send_chunk():  # 流式读取
        store_path = saveDir + '%s' % filename
        print("store is ",store_path)
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk
    return Response(send_chunk(), content_type='application/octet-stream')

@app.route('/',defaults={'filename': None}, methods=['POST'])
@app.route('/<path:filename>', methods=['POST'])
def upload_part(filename):  # 接收前端上传的一个分片
    saveDirN = saveDir
    print("filename is ",filename)
    if filename != None:
        saveDirN = saveDir + '/' + filename + '/'
    saveName = request.form.get('name')  # 获取文件的唯一标识符
    chunks = request.form.get('chunks')  # 获取该分片在所有分片中的序号
    chunk = request.form.get('chunk')  # 获取该分片在所有分片中的序号
    if chunks != None:
        saveName = '%s_%s' % (saveName, chunk)  # 构造该分片的唯一标识符
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
    if int(chunk) == (int(chunks)-1):
        target_filename = request.form.get('name')  # 获取上传文件的文件名
        # task = request.args.get('task_id')  # 获取文件的唯一标识符
        chunk = 0  # 分片序号
        with open(saveDirN + '%s' % target_filename, 'wb') as target_file:  # 创建新文件
            while True:
                try:
                    filename = saveDirN + '%s_%s' % (target_filename, chunk)
                    source_file = open(filename, 'rb')  # 按序打开每个分片
                    target_file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                except Exception as e:
                    # print("error is ",e)
                    break
                chunk += 1
                os.remove(filename)  # 删除该分片，节约空间
        print("upload all chunks saveas ",target_filename)
    return str(0)
    return rt('./index.html')

if __name__ == '__main__':
    app.run(debug = True)