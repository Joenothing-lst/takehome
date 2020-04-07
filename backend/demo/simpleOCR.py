from flask import Flask ,request ,render_template
from aip import AipOcr
from typing import Optional ,List
import json
#构造百度ocr client对象

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

#Cerat baidu ocr client object
bd_ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
ALLOWED_EXTENSIONS = ['jpg','png']
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simpleOCR',methods = ['GET', 'POST'])
def simpleOCR():
    return render_template('simpleOCR.html')

@app.route('/OCR_api',methods = ['GET', 'POST'])
def OCR_api():
    if request.method == 'POST' and request.files.get('file'):
        f = request.files['file']
        byte=f.read()
        result=get_img_content(byte)
        filename=f.filename
        set_database(byte,filename,result)
        return result
    return render_template('simpleOCR.html')

#Check payload file name.(Prevent frontend code being changed by user).
def allowed_file(filename) -> Optional[bool]:
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

#baidu OCR api.
def get_img_content(img) -> List[int or str]:
    result = bd_ocr_client.basicAccurate(img)
    m={}
    if result.get('words_result'):
        m['content'] = [i['words'] for i in result['words_result']]
    else :
        m['content'] = -1
    return json.dumps(m,ensure_ascii=False)

#save to database(MySQL)
def set_database(b,fn,r):
    try:
        # Please write your MySQL's information.
        conn = pymysql.connect(
            host='localhost', user='root', passwd='123456', db='simpleOCR', charset='utf8')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO simpleOCR_result(bytes,filename,result) VALUES ({b},{fn},{r})')
        conn.commit()
    except Exception as e:
        print(e)
    return None


if __name__ == '__main__':
    app.run()

