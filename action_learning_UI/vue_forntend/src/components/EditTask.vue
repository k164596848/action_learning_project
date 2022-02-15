<template>
  <form @submit="onSubmit" class="add-form">
    <div class="form-control">
      <label>Action</label>
      <input
        type="text"
        name="text"
        id="text"
        :value="show_updtask.text"
        placeholder="the action name"
      />
    </div>

    <div class="form-control">
      <label>Weight List={{  show_updtask.weight }} </label>
      <label>Json path={{  show_updtask.jsonpath }} </label>
    </div>

    <div
      :key="test_part"
      v-for="test_part in show_updtask.test_parts"
      class="form-control form-control-check"
    >
      <label>{{ test_part.name }}</label>
      <input
        type="checkbox"
        @click="clickCheckbox(test_part.name)"
        :id="test_part.name + '_edit'"
        :checked="test_part.weight_value"
      />
      <input
        type="text"
        :id="test_part.name + '_input'"
        :value="test_part.weight_value"
        :placeholder="test_part.weight_value"
      />
    </div>
    

    <input
      type="submit"
      value="Update Action"
      class="btn btn-block"
      style="background: green"
    />
    <img src="../assets/openpose.png" />
  </form>
</template>

<script>
export default {
  name: "EditTask",
  props: {
    show_updtask: Array,
  },
  data() {
    return {
      text: "",
      weight: "",
      joints_variable: {
        left_shoulder: "",
        right_shoulder: "",
        left_arm: "",
        right_arm: "",
        left_knee: "",
        right_knee: "",
      },
      reminder: false,
      parts: {
        left_shoulder: "",
        right_shoulder: "",
        left_arm: "",
        right_arm: "",
        left_knee: "",
        right_knee: "",
      },
      video:new FormData,
    };
  },
  methods: {
    
    onSubmit(e) {
      e.preventDefault();
      
      //state:將action名稱讀取
      const input_text = document.getElementById("text").value;
      if (input_text !== this.show_updtask.text) this.text = input_text;
      else this.text = this.show_updtask.text;
      // state:檢查action name 是否為empty
      if (!this.text) {
        alert("Please typing an action ");
        return;
      }

      //state check referrence video
      if (!this.text) {
        alert("Please upload an action ");
        return;
      }

      // state: put weight value in a list
      var weight_list = [];
      for (var joint in this.parts) {
        var joint_value = document.getElementById(joint + "_input").value;
        weight_list.push(parseFloat(joint_value));
        console.log(joint, joint_value);
      }


      // state:打包整個
      const updateTask = {
        id: this.show_updtask.id, //原生ID
        text: this.text, //輸入的Action name
        weight: weight_list, //
        reminder: this.reminder,
        left_shoulder: parseFloat(weight_list[0]),
        right_shoulder: parseFloat(weight_list[1]),
        left_arm: parseFloat(weight_list[2]),
        right_arm: parseFloat(weight_list[3]),
        left_knee: parseFloat(weight_list[4]),
        right_knee: parseFloat(weight_list[5]),
        jsonpath:this.show_updtask.jsonpath
      };
      // state:上傳相關資料
      this.updateTask(updateTask);

      //state:上傳


      // state: 清空值
      this.text = "";
      this.weight = "";
      this.reminder = false;

      alert("update finished");

      location.reload();
    },
    async updateTask(updTask) {
      const res = await fetch(`http://localhost:5001/tasks/${updTask.id}`, {
        method: "PUT",
        //header"s"有s
        headers: {
          "Content-type": "application/json",
        }, 
        body: JSON.stringify(updTask),
      });
      //await 記得加上去
      const data = await res.json(updTask);
      console.log(data);
      //用map將對應到的task.id 的reminder key 做not 運算，並且替換掉
      // this.tasks = this.tasks.map((task) =>
      //   task.id === id ? { ...task, reminder: data.reminder } : task
      // );

      document.getElementById("text").value = "";
    },
    clickCheckbox(part_name) {
      var joint_checkbox = document.getElementById(part_name + "_edit").checked;
      if (joint_checkbox) {
        document.getElementById(part_name + "_input").value = 1;
      } else {
        document.getElementById(part_name + "_input").value = 0;
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
.btn {
  display: inline-block;
  background: rgb(58, 235, 211);
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin-left: 30%;
  margin-bottom: 5%;
  margin-top: 5%;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
}
.btn-block {
  display: block;
  width: 40%;
}
</style>