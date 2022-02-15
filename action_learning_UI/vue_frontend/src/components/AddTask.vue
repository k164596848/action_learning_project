<template>

  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>Action</label>
      <input
        type="text"
        v-model="text"
        name="text"
        placeholder="Add Action name"
      />
    </div>
    <p>-----------</p>
    <div
      class="form-control form-control-check"
      :key="part"
      v-for="part in parts"
    >
      <label>{{ part }}</label>
      <input @click="clickCheckbox(part)" type="checkbox" :id="part"/>
      <input type="text" :id="part+'_addinput'"  placeholder="0" />
    </div>
    
    <div class="input-group">
      <input
        type="file"
        name="file"
        class="form-control"
        id="inputGroupFile04"
        aria-describedby="inputGroupFileAddon04"
        aria-label="Upload"
        @change="fileChange"
      />
     
    </div>

    <input type="submit" value="Add Action" class="btn btn-block" />
    <br>
    <img src="../assets/openpose.png"/>
  </form>
  
  
</template>

<script>
export default {
  name: "AddTask",
  props: {},
  data() {
    return {
      text: "",
      weight: "",
      left_shoulder: "",
      right_shoulder: "",
      left_arm: "",
      right_arm: "",
      left_knee: "",
      right_knee: "",
      reminder: false,
      parts: {
        left_shoulder: "left_shoulder",
        right_shoulder: "right_shoulder",
        left_arm: "left_arm",
        right_arm: "right_arm",
        left_knee: "left_knee",
        right_knee: "right_knee",
      },
      video: new FormData(),
    };
  },
  methods: {
    fileChange(e) {
      this.video.append('file', e.target.files[0]) //放進上傳的檔案
    },
    async onSubmit(e) {
      e.preventDefault();

      // state:檢查action name 是否為empty
      if (!this.text) {
        alert("Please add a action");
        return;
      }

      
      // state:check the reff viedo is empty or not ?
      if (this.video.get("file")===null) {
        alert("Please upload a video");
        return;
      }
      this.video.append('name',this.text );
    

      // state: put weight value in a list
      var add_weight_list = []
      for (var joint in this.parts){
        var joint_value =document.getElementById(joint+"_addinput").value
        if(joint_value===""){joint_value=0}
        add_weight_list.push(parseFloat(joint_value))
      }
     

      const newTask = {
        id: this.id + 1,
        text: this.text,
        weight: add_weight_list,
        left_shoulder: parseFloat(add_weight_list[0]),
        right_shoulder: parseFloat(add_weight_list[1]),
        left_arm: parseFloat(add_weight_list[2]),
        right_arm: parseFloat(add_weight_list[3]),
        left_knee:parseFloat( add_weight_list[4]),
        right_knee: parseFloat(add_weight_list[5]),
        reminder: this.reminder,
        jsonpath:"flask_backend/json/"+this.text
      };
      
      

      await this.$emit("add-task",newTask);

      
      await this.upload_video(this.video);
      
      
      

      //清空值
      (this.text = ""), (this.weight = ""), (this.reminder = false);
      for (var part in this.parts){
        // document.getElementById(part+"input").value=0
        console.log(part);
      }
      setTimeout(function(){
        location.reload();
      }, 1000);
      
    },
    async upload_video(video){
      const axios = require('axios').default;
      axios.post('http://127.0.0.1:5000/uploader', video)
      alert("add new video is success !");
      
    },
    clickCheckbox(part_name){
      var joint_checkbox =document.getElementById(part_name).checked;
      if(joint_checkbox){
        document.getElementById(part_name+'_addinput').value=1  
      }
      else{
        document.getElementById(part_name+'_addinput').value=0
      }
    },
  },
  
};
</script>

<style scoped>
.add-form {
  margin-bottom: 40px;
}
.form-control {
  margin: 20px 0;
}
.form-control label {
  display: block;
}
.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px;
  padding: 3px 7px;
  font-size: 17px;
}
.form-control-check {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.form-control-check label {
  flex: 1;
}
.form-control-check input {
  flex: 2;
  height: 20px;
}
</style>