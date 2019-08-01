<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1 align="center">TASK LIST</h1>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Step</th>
              <th scope="col">Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, index) in tasks" :key="index">
              <td>{{ task.name }}</td>
              <td>{{ task.step }}</td>
              <td>{{ task.status }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Start</button>
                  <button type="button" class="btn btn-success btn-sm" onclick="location.href='http://localhost:8080/Results'">Result</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
<b-navbar-nav>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.task-modal>Add Order</button>
      </b-navbar-nav>
      </div>
    </div>
    <b-modal ref="addTaskModal"
            id="task-modal"
            title="Add a new task"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Name:"
                    label-for="form-title-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addTaskForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-step-group"
                      label="Step:"
                      label-for="form-step-input">
            <b-form-input id="form-step-input"
                          type="text"
                          v-model="addTaskForm.step"
                          required
                          placeholder="Enter step">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-file-group"
                      label="Upload File:"
                      label-for="form-file-input">
            <b-form-file
                accept=".xlsx"
                type="file" 
                id="file" 
                ref="file" 
                v-on:change="onhandleFileUpload()"
                v-model="file"
                :state="Boolean(file)"
                placeholder="Choose a file..."
                drop-placeholder="Drop file here..."
            ></b-form-file>
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button id="submit "type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: '',
      tasks: [],
      addTaskForm: {
        name: '',
        step: null,
        user : '',
        file:'',
        status:'Not Started'
      },
    };
  },
  methods: {
    getTasks() {
      const path = 'http://localhost:5000/json';
      axios.get(path)
        .then((res) => {
          this.tasks = res.data.tasks;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTask(payload) {
      const path = 'http://localhost:5000/json';
      axios.post(path, payload)
        .then(() => {
          this.getTasks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getTasks();
        });
    },
    initForm() {
      this.addTaskForm.name = '';
      this.addTaskForm.step = null;
      this.addTaskForm.status = '';
      this.addTaskForm.user = '';
      this.addTaskForm.file = '';
    },
    onhandleFileUpload(){
      this.file = this.$refs.file.files[0];
    },
    onSubmit(evt) {
      const path = 'http://localhost:5000/json-file';
      var formData = new FormData();
console.log(this.file);
formData.append("test", "testice");
console.log(formData);
      axios.post( path,
          formData,
          {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
        }
      ).then(function(){
    console.log('SUCCESS!!');
  })
  .catch(function(){
    console.log('FAILURE!!');
  });
      evt.preventDefault();
      this.$refs.addTaskModal.hide();
      const payload = {
        name: this.addTaskForm.name,
        step: this.addTaskForm.step,
        status: this.addTaskForm.status,
        file: this.addTaskForm.file,
        user: this.addTaskForm.user,
      };
      this.addTask(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTaskModal.hide();
      this.initForm();
    },
  },
    created() {
      this.getTasks();
  },
};
</script>
