from flask import Flask, request, jsonify,render_template
from os import makedirs
import requests
import json
from flask_cors  import CORS
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response as responses
from refvideo import save_to_json_path



app = Flask(__name__)
CORS(app)



##
@app.route('/',methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/multipleperson',methods=['GET', 'POST'])
def multipleperson():
    if request.method == "POST":

        print(request.form.keys())

        txtfile= open('yourip.txt', 'r',encoding='utf-8')
        your_ip =txtfile.read()
        
        response  = requests.post("http://"+ str(your_ip) +":8080/multipleperson/",
        files = {
            "video":request.files['file'],
            'person':request.form['person'],
            'gender':request.form['gender'],
            'age':request.form['age']
        })

        print(response.json())
        return('success', 204)

@app.route('/upload_tester',methods=['GET', 'POST'])
def upload_tester():
    if request.method == 'POST':
        f = request.files['file']
        
        # print(request.files.keys())
        print(request.form.keys())
        print(request.form['age'])

        txtfile= open('yourip.txt', 'r',encoding='utf-8')
        your_ip =txtfile.read()
        

        response  = requests.post('http://'+ str(your_ip) +':8080/fitness/'+ request.form['action'] +'/',
            files={
                "video":request.files['file'],
                'gender':request.form['gender'],
                'age':request.form['age'],
                'pointIndex':13,
                'action':request.form['action']
            }
        
        )
        print(response.json())
    # return ('success', 204)
    return (response.json())



@app.route('/coach')
def coach():
    txtfile= open('yourip.txt', 'r',encoding='utf-8')
    your_ip =txtfile.read()

    r =requests.get('http://'+ str(your_ip) +':8080/action/coach/')

    print(r.json())

    return ('success', 204)

@app.route('/upload',methods=['GET'])
def upload():

    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
async def upload_file():
    if request.method == 'POST':
        path="video\\"
      
        
        f = request.files['file']
        f.filename = request.form['name']+ f.filename[(len( f.filename)-4):len(f.filename)]
        
        video_name=str(f.filename)
        f.save(path+f.filename)

        # f.save(path+secure_filename(f.filename))
        
    video_path =path+(f.filename)

    #先進行新增資料夾,using the video name to create new folder
    try:
        filename =str(f.filename)
        folder_path="json/"+ filename[0:(len(filename)-4)]
        makedirs(folder_path)
    except FileExistsError:
        pass
    await save_to_json_path(video_path, folder_path, hand=True)
    
    return ('success', 204)
       

@app.route('/otherpage/',methods=['GET'])
def otherpage():
    return render_template('copy.html')

@app.route('/tasks', methods=['GET','OPTIONS',"PSOT"])
def get_tasks():
    path= "../vue_forntend/db.json"
    json_data = json.load(open(path,encoding='utf-8'))
    
    tasks = json_data['tasks']
    # print(data)

    return jsonify(json_data)
    # return jsonify(tasks) 



if __name__ == "__main__":
    app.run(debug=True)
    
    