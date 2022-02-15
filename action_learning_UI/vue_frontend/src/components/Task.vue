<template>
  <div :id="task.id"
  @dblclick="$emit('toggle-reminder',task.id);$emit('show-update-task',task );$emit('showEditTask');"
  :class="[task.reminder ? 'reminder' : '','task']">
    <h3>{{ task.text }} 
        <i @click="onDelete(task.id)" class="fas fa-times"></i>
        
    </h3>
    <p>{{ task.weight }}</p>
  </div>

      
</template>



<script>
export default {
  name: "Task",
  props: {
    task: Array,
    
  },
  
  methods:{
      onDelete(id){
          this.$emit("delete-task",id)
      }

  }
};
</script>

<style scope>
.fas {
  color: red;
}
.task {
  background: #f4f4f4;
  margin: 5px;
  padding: 10px 20px;
  cursor: pointer;
}
.task.reminder {
  border-left: 5px solid green;
}
.task h3 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>