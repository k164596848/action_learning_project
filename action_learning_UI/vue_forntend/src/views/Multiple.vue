<template>
  <div>
    <form v-show="showform">
      <div class="mb-3">
        <h3 for="person">How many person you have</h3>
        <select
          class="form-select form-select-lg mb-3"
          aria-label=".form-select-lg example"
          id="person"
          v-model="person"
        >
          <option value="1">1 person</option>
          <option value="2">2 person</option>
          <option value="3">3 person</option>
          <option value="4">4 person</option>
          <option value="5">5 person</option>
        </select>
      </div>

      <div class="mb-3">
        <h3>Upload Testers video</h3>
        <input
          class="form-control"
          type="file"
          name="file"
          id="formFile"
          @change="fileChange"
        />
      </div>

      <div class="mb-3">
        <h3>Theirs Gender</h3>
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
        <h3>Theirs Age</h3>
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

    <img v-show="showloading" src="../assets/loading1.gif" alt="" />
  </div>
</template>


<script>
export default {
  name: "Multiple",
  props: {},
  data() {
    return {
      showloading: false,
      showform: true,

      person: "",
      age: "",
      gender: "",
      data: new FormData(),
    };
  },
  methods: {
    fileChange(e) {
      this.data.append("file", e.target.files[0]); //放進上傳的檔案
    },
    async onSubmit(e) {
      e.preventDefault();
      this.data.append("person", this.person);
      this.data.append("gender", this.gender);
      this.data.append("age", this.age);


      this.showform = false;
      this.showloading = true;

      const axios = require("axios").default;
      axios
        .post("http://127.0.0.1:5000/multipleperson", this.data)
        .then(response=> {
          console.log(response);
          this.showform = true;
          this.showloading = false;
        })
        .catch(error=> {
          console.log(error);
        });
    },
  },
};
</script>

