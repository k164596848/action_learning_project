# action_learning_UI

## Update 
- need to manully click link to show the result video, because Vue will find the video path before the result video generate at compile stage. It make the requrie usally can not find the source  and report the Error.

###  develop environment
- Visual Studio Code
- Node js 
- Python 3.7 + (recommend the 3.7)
- to check the python and pip version you can use the following cmd
```bash
python -V  
pip -V
```

### Node js 
- please install [Node.js](https://nodejs.org/zh-tw/download/) , the version is node-v14.17.1-x64.msi   
- open VSCode, Nodejs and install some packages, more detail pls see [npm_requirement](vue_frontend/npm_requirement.txt) 

```bash
cd vue_frontend
npm install "packages name"
```
- if you want to study more detail about VUE .js 
- you can see this tutorial video [Vue JS Crash Course 2021](https://www.youtube.com/watch?v=qZXt1Aom3Cs)
- the [Vue cli](https://cli.vuejs.org/migrating-from-v3/) document , let you know the VUE Command Line Interface 
- use  following cmd
```bash
cd vue_frontend
npm install vue@next
npm i -g @vue/cli
npm i -g json-server
npm i -g vue-router@next
npm install axios
npm install cors
```



### Python Flask frame
- using pip to install the python packages 
``` bash
cd flask_backend
pip install flask
pip install flask_cors
pip install requests
``` 

### Setting your personal IP
- setting your personal IP in the [yourip.txt](), you can use the [ipconfig]() cmd to comfirm yor ip on the Windows cmd interface.
```bash
ipconfig
```

### Run the user interface 
- first , make sure the port 8080, 5000, 3000, 5001 is avaliable
- open a new  terminal in the ***vue_frontend*** folder in the action_learning_UI folder
- when first activate ***vue_frontend*** you should use "[npm run build]()" cmd to create the dist folder.
```bash
npm run serve
npm run build    #(first time use)
```
- open another terminal in the same folder ***(vue_frontend)*** in the action_learning_UI folder
```bash
npm run jsonserver
```


- open new terminal in the ***flask_backend*** folder in the action_learning_UI folder
```bash
python app.py
```

- avtivate the core system, open terminal on the ***action-learning*** folder.
```
python app.py
```

### ???????????? ??????
1. ?????????????????????????????????
2. ??????????????????(10~20 ???)???????????????
3. ???????????????????????????????????????????????????????????????
4. ??????????????????45??????????????????????????????????????????
5. ??????????????????????????????????????????????????????(??????????????????????????????)
6. ??????????????????????????????????????????????????????????????????????????????????????????????????????


### the VUEjs packages structure
```
????????? @vue/cli-plugin-babel@4.5.13
????????? @vue/cli-plugin-eslint@4.5.13
????????? @vue/cli-service@4.5.13
????????? @vue/compiler-sfc@3.1.2
????????? axios@0.21.1
????????? babel-eslint@10.1.0
????????? bindings@1.5.0 extraneous
????????? core-js@3.15.2
????????? cors@2.8.5
????????? eslint-plugin-vue@7.12.1
????????? eslint@6.8.0
????????? file-uri-to-path@1.0.0 extraneous
????????? json-server@0.16.3
????????? nan@2.14.2 extraneous
????????? vue-router@4.0.10
????????? vue@3.1.2
```

