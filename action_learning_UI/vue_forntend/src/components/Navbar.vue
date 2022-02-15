<template>
  <header>
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <router-link class="nav-link" to="/home">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/uploadrefvideo"
          >Upload reference video</router-link
        >
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/multiple_person">Multiple Person</router-link>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true"
          >Result Log</a
        >
      </li>
    </ul>
  </header>
</template>


<script>
export default {
  name: "Navbar",
  props: {

  },
  
  methods:{
     

  }
};
</script>