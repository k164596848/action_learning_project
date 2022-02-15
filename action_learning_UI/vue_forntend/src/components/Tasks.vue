<template>
  <!-- 使用 v-for的方式將 cycle完成 -->
  <div>
    <div :key="task.id" v-for="task in tasks">
      <Task
        @toggle-reminder="$emit('toggle-reminder', task.id)"
        @delete-task="$emit('delete-task', task.id)"
        @showEditTask="showEditTaskVue"
        @show-update-task="passUpdateTask"
        :task="task"
      />
    </div>
    <div>
      <EditTask :show_updtask="update_task" v-show="show_editTask" />
    </div>
  </div>
</template>

<script>
import Task from "./Task";
import EditTask from "./EditTask";

export default {
  name: "Tasks",
  props: {
    tasks: Array,
  },
  data() {
    return {
      show_editTask: false,
      update_task: [],
    };
  },
  components: {
    Task,
    EditTask,
  },
  emits: ["delete-task", "toggle-reminder", "update-task"],
  methods: {
    showEditTaskVue() {
      this.show_editTask = true;
    },
    passUpdateTask(task) {
      //只能取到子元件的值，不能傳值過去
      // EditTask.data().text =task.text

      const modify_task = {
        id: task.id,
        text: task.text,
        weight: task.weight,
        reminder: task.reminder,
        left_shoulder: task.left_shoulder,
        right_shoulder: task.right_shoulder,
        left_arm: task.left_arm,
        right_arm: task.right_arm,
        left_knee: task.left_knee,
        right_knee: task.right_knee,
        jsonpath: task.jsonpath,
        test_parts: [
          {
            name: "left_shoulder",
            weight_value: task.left_shoulder,
          },
          {
            name: "right_shoulder",
            weight_value: task.right_shoulder,
          },
          {
            name: "left_arm",
            weight_value: task.left_arm,
          },
          {
            name: "right_arm",
            weight_value: task.right_arm,
          },
          {
            name: "left_knee",
            weight_value: task.left_knee,
          },
          {
            name: "right_knee",
            weight_value: task.right_knee,
          },
        ],
        
      };

      this.update_task = modify_task;
    },
  },
};
</script>