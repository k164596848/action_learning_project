<template>
  <div>
    <form v-show="showform">
      <div class="mb-3">
        <h3 for="action">Action</h3>
        <select
          class="form-select form-select-lg mb-3"
          aria-label=".form-select-lg example"
          id="action"
          v-model="action"
        >
          <option value="原地站立抬膝">原地站立抬膝</option>
          <option value="肱二頭肌手臂曲舉">肱二頭肌手臂曲舉</option>
          <option value="椅子坐立">椅子坐立</option>
        </select>
      </div>

      <div class="mb-3">
        <h3>Upload tester video</h3>
        <input
          class="form-control"
          type="file"
          name="file"
          id="formFile"
          @change="fileChange"
        />
      </div>

      <div class="mb-3">
        <h3>Gender</h3>
        <select
          class="form-select form-select-lg mb-3"
          aria-label=".form-select-lg example"
          id="gender"
          v-model="gender"
        >
          <option value="男">男</option>
          <option value="女">女</option>
        </select>
      </div>

      <div class="mb-3">
        <h3>Age</h3>
        <select
          class="form-select form-select-lg mb-3"
          aria-label=".form-select-lg example"
          id="age"
          name="age"
          v-model="age"
        >
          <option value="65">65</option>
          <option value="70">70</option>
          <option value="75">75</option>
          <option value="80">80</option>
          <option value="85">85</option>
          <option value="90">90</option>
        </select>
      </div>

      <button type="submit" @click="onSubmit" class="btn btn-primary">
        Submit
      </button>
    </form>

    <img v-show="showloading" src="../assets/loading.gif" alt="" />

    <div v-show="showresult">
      <ul class="list-group list-group-flush">
        <li class="list-group-item">Result</li>
        <li class="list-group-item">動作: {{ retrunAction }}</li>
        <li class="list-group-item">年齡: {{ retrunAge }}</li>
        <li class="list-group-item">性別: {{ retrunGender }}</li>
        <li class="list-group-item">程度: {{ retrunLevel }}</li>
        <li class="list-group-item">Path: {{ retrunVideoPath }}</li>
        <a :key="reLoad" href="" @click="changeLoad">click here to show Output_video</a>        
      </ul>

      <video v-if="reLoad" width="320" height="240" controls>
        <source :key="reLoad" :src="reLoad ? (`${retrunVideoPath}`) : retrunVideoPath" type="video/mp4">
        
        
      </video>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  props: {},
  data() {
    return {
      showloading: false,
      showform: true,
      showresult: false,
      reLoad:false,

      tempvideopath:"",
      retrunVideoPath: "",
      retrunAge: "",
      retrunGender: "",
      retrunAction: "",
      retrunLevel: "",

      action: "",
      gender: "",
      age: "",
      pointIndex: "13",

      tester_data: new FormData(),
    };
  },
  components: {},
  methods: {
    fileChange(e) {
      this.tester_data.append("file", e.target.files[0]); //放進上傳的檔案
    },
    async onSubmit(e) {
      e.preventDefault();
      if (this.action == "原地站立抬膝") {
        this.pointIndex = 13;
      }
      this.tester_data.append("action", this.action);
      this.tester_data.append("gender", this.gender);
      this.tester_data.append("age", this.age);
      this.tester_data.append("pointIndex", this.pointIndex);

      this.showform = false;
  
      this.showloading = true;// showloading:等待結果的GIF

     
      

      const axios = require("axios").default;
      await axios
        .post("http://127.0.0.1:5000/upload_tester", this.tester_data)
        .then((response) => {
          console.log(response.data);
          console.log(response.data["年齡"]);
          console.log(response.data["性別"]);
          console.log(response.data["video"]);
          this.retrunAge = response.data["年齡"];
          this.retrunGender = response.data["性別"];
          this.retrunAction = response.data["動作"];
          this.retrunLevel = response.data["程度"];
          this.tempvideopath =  response.data["video"];
          this.retrunVideoPath =
            "../../../../action-learning/stativ/out/"+response.data["video"];
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          this.showform = true;
          this.showresult = true;
          this.showloading = false;
          
        });

      // const res = await fetch(
      //   `http://127.0.0.1:5000/upload_tester`,
      //   {
      //     method: "POST",
      //     body:{
      //         video: this.tester_video,
      //         gender: this.gender,
      //         age: this.age,
      //         pointindex: this.pointindex
      //     }

      //   }
      // );

      // const data = await res.json();

      // console.log(data);
    },
    recoverForm() {
      this.showform = true;
      this.showloading = false;
      
    },
    changeLoad(e){
      e.preventDefault();
      this.reLoad=true;
      if(this.reLoad){
        this.retrunVideoPath=require("../../../../action-learning/static/out/"+`${this.tempvideopath}`);
      }
      
      console.log(this.reLoad);
      console.log(this.retrunVideoPath);
      console.log(this.tempvideopath);
    },

  },
  
};
</script>