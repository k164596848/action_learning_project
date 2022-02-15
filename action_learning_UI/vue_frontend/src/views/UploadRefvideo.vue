<template>
 <div>
    <h1> Upload the reference video</h1>   
    <Button
      @btn-click="toggleAddTask"
      :text="showAddTask ? 'Close' : 'Add Reference Action'"
      :color="showAddTask ? 'red' : 'green'"
    />

    <AddTask
      v-show="showAddTask"
      @add-task="addTask"
      :showAddTask="showAddTask"
    />
    
    
    <Tasks
      @toggle-reminder="toggleReminder"
      @delete-task="deleteTask"
      :tasks="tasks"
    />
   </div> 
</template>

<script>
import Button from '../components/Button';
import Tasks from "../components/Tasks";
import AddTask from "../components/AddTask";

export default {
  name: "UploadRefvideo",
  props: {
      show_AddTask:Boolean,
  },
  components: {
    Button,
    Tasks,
    AddTask,
  },
  data() {
    return {
      tasks: [],
      showAddTask: false,
    };
  },
  methods: {
    toggleAddTask() {
      this.showAddTask = !this.showAddTask;
    },
    async addTask(task) {
      //#...this.task可能是目前的tasks, 後面的task是想要新增進去的
      const res = await fetch("http://localhost:5001/tasks", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          //不要將body 放到headers 要注意
        },
        body: JSON.stringify(task),
      });

      const data = await res.json();

      //原本的後面是task
      // this.tasks = [...this.tasks,task]
      //使用json server 後task替換成data
      this.tasks = [...this.tasks, data];
    },
    async deleteTask(id) {
      if (confirm("Are you sure to delete this action?")) {
        const res = await fetch(`http://localhost:5001/tasks/${id}`, {
          method: "DELETE",
        });

        res.status === 200
          ? (this.tasks = this.tasks.filter((task) => task.id !== id))
          : alert("Error delete!!");
      }
    },
    async toggleReminder(id) {
      //使用類似的functoin 處理
      const taskToToggle = await this.fetchTask(id); //先撈出該筆資料

      //將改過狀態的reminder值先另存起來
      const updTask = { ...taskToToggle, reminder: !taskToToggle.reminder };
      // document.getElementById("weight").value= updTask.weight
      // document.getElementById("text").value=updTask.text

      const res = await fetch(`http://localhost:5001/tasks/${id}`, {
        method: "PUT",
        //header"s"有s
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(updTask),
      });
      //await 記得加上去
      const data = await res.json();
      //用map將對應到的task.id 的reminder key 做not 運算，並且替換掉
      this.tasks = this.tasks.map((task) =>
        task.id === id ? { ...task, reminder: data.reminder } : task
      );
      this.tasks = await this.fetchTasks();
    },
    // 此處是定義API的地方
    async fetchTasks() {
      // const axios = require('axios').default;
      // axios.get('http://localhost:5000/tasks')
      // .then(function (response) {
      //   // handle success
      //   console.log(response.data.tasks);
      //   console.log("axios success");
      // })

      const res = await fetch(`http://localhost:5000/tasks`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await res.json();

      // console.log(data.tasks)
      return data.tasks;
      // return data;
    },
    async fetchTask(id) {
      const res = await fetch(`http://localhost:5001/tasks/${id}`);

      const data = await res.json();
      return data;
    },
  },
  
  async created() {
    this.tasks = await this.fetchTasks();
  },
};
</script>