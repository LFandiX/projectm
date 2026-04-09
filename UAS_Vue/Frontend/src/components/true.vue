<script>
    import axios from 'axios';
    export default {
    name: 'Dashboard',
    data() {
    return {
        editingTaskId: null,
        form: {
            hari: '',
            judul: '',
            date: '',
            Kategori:'',
            deskripsi:''
        },
        form1: {
            hari: '',
            judul: '',
            date: '',
            Kategori:'',
            deskripsi:''
        },
        showForm: false,
        showForm1: false,
        showlistTask: false,
        showUrgent: false,
        showImportant: false,
        showReguler: false,
        showedit: true,
        task:[],
        selectedKategoriFilters: []


    }   
    },
    mounted() {
      this.fetchTask(); // langsung load task ketika dashboard ditampilkan
    },

    watch: {
      selectedKategoriFilters(newVal) {
        // Jika semua Kategori aktif, centang "All"
        if (
          newVal.includes('Important') &&
          newVal.includes('Urgent') &&
          newVal.includes('Reguler') &&
          newVal.length === 3
        ) {
          this.selectAll = true;
        } else {
          this.selectAll = false;
        }
      }
    },

    methods: {
      async submitForm() {
        try {
          if (this.editingTaskId === null) {
            const response = await axios.post('http://localhost:5000/api', this.form);
            console.log('Data berhasil dikirim:', response.data);
            alert('Tugas berhasil dikirim!');
          } else {
            const response = await axios.put(`http://localhost:5000/api/${this.editingTaskId}`, this.form);
            console.log('Data berhasil diedit:', response.data);
            alert('Tugas berhasil diedit!');
          }

              // Reset form & state
              this.form = {
                hari: '',
                judul: '',
                date: '',
                Kategori: '',
                deskripsi: ''
              };
              this.editingTaskId = null;
              this.showForm = false;

              // Refresh data
              this.fetchTask();

            } catch (error) {
              console.error('Gagal submit form:', error);
              alert('Terjadi kesalahan saat menyimpan data.');
            }
          },    

      async submitForm1() {
        try {
            const response = await axios.put(`http://localhost:5000/api/${this.editingTaskId}`, this.form1);
            console.log('Data berhasil diedit:', response.data);
            alert('Tugas berhasil diedit!');
            // Reset form & state
            this.form1= {
              hari: '',
              judul: '',
              date: '',
              Kategori: '',
              deskripsi: ''
            };
            this.editingTaskId = null;
            this.showForm1 = false;

            // Refresh data
            this.fetchTask();

          } catch (error) {
            console.error('Gagal submit form:', error);
            alert('Terjadi kesalahan saat menyimpan data.');
          }
        },

      fetchTask() {
          // this.showlistTask != this.showlistTask
          let http = axios.create({
          baseURL: "http://127.0.0.1:5000",
          headers: {
              "Content-Type": "application/json",
              "Accept" : "application/json"
          }
          })
          
          http.get("/api")
          .then((response) => {
              // Simpan semua data yang diperlukan
              this.task = response.data;
              console.log("Response:", response);
              console.log(this.tasks);
          })
          .catch((error) => {
              console.error("Error fetching posts:", error);
            });
          },
          
      async markAsDone(taskId) {
          try {
            await axios.put(`http://localhost:5000/api/${this.editingTaskId}/done`);
            this.editingTaskId = null;
            this.showForm1 = false;
            console.log('Task berhasil ditandai selesai');
            alert('Task berhasil ditandai selesai');
            this.fetchTask();
          } catch (error) {
            console.error("Gagal tandai selesai:", error);
            alert('Terjadi kesalahan saat menandai task sebagai selesai.');
          }
        },
        
      async deleteTask(taskId) {
          try {
            await axios.delete(`http://localhost:5000/api/${taskId}`);
            this.fetchTask();
            this.showForm1 = false;
            console.log('Task berhasil dihapus');
            alert('Task berhasil dihapus');
      
          } catch (error) {
            console.error("Gagal menghapus task:", error);
            alert('Terjadi kesalahan saat menghapus data.');
          }
        },

      getKategoriClass(Kategori,status) {
        return {
          done: status === "Done",
          important: Kategori === "Important",
          urgent: Kategori === "Urgent",
          reguler: Kategori === "Reguler",
          
        };
      },

      filteredPostsByDay(day) {
        let filtered = this.task.filter(post => post.hari === day && post.status !== 'Deleted');
        if (this.selectedKategoriFilters.length > 0 ) {
          filtered = filtered.filter(post =>
            this.selectedKategoriFilters.includes(post.Kategori)
          );
        }
      
        // if no filters selected, show all posts for that day
        return filtered;
      },

      toggleAll() {
        if (this.selectAll) {
          // If "All" is checked, clear other selections
          this.selectedKategoriFilters = ['Important', 'Urgent', 'Reguler'];
        } else {
          // If "All" is unchecked, clear the selection
          this.selectedKategoriFilters = [];
        }
      },

      startEditing(post) {
        this.editingTaskId = post.id;
        let date = new Date(post.date);
        let formattedDate = date.toISOString().split('T')[0]; // Format YYYY-MM-DD
        this.form1 = {
          hari: post.hari,
          judul: post.judul,
          date: formattedDate,
          Kategori: post.Kategori,
          deskripsi: post.deskripsi
        };
        
        // kalau form add task terbuka > matikan dulu:
        if (this.showForm == true) {
          this.showForm = false;
        };

        this.showForm1 = true;
    },


    formatDate(dateStr) {
      const date = new Date(dateStr);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    },
    closeform() {
      this.showForm = false;
      this.form = {
        hari: '',
        judul: '',
        date: '',
        Kategori:'',
        deskripsi:''
      };
      this.editingTaskId = null;
    },
    closeform1() {
      this.showForm1 = false;
      this.form1 = {
        hari: '',
        judul: '',
        date: '',
        Kategori:'',
        deskripsi:''
      };
      this.editingTaskId = null;
    },
  }
    }


</script>


<template>
  <main class="dashboard-page">
    <div class="background-web">

      <!-- bagian atas -->
      <div class="toolbar">

        <!-- Bagian Filter Data  -->
        <div class="filter-container">
          <label id="important-task">
            <input type="checkbox" value="Important" v-model="selectedKategoriFilters" />
            Important
          </label>
          <label id="urgent-task">
            <input type="checkbox" value="Urgent" v-model="selectedKategoriFilters" />
            Urgent
          </label>
          <label id="reguler-task">
            <input type="checkbox" value="Reguler" v-model="selectedKategoriFilters" />
            Regular
          </label>
          <label id="all-task">
            <input type="checkbox" v-model="selectAll" @change="toggleAll" />
            All
          </label>
          <label id="all-task">
            <input type="checkbox" v-model="selectAll" @change="toggleAll" />
            All
          </label>
        </div>

        <button @click="showForm = !showForm" id="add-task">+</button>
      </div>

      <transition name="slide">
        <div v-if="showForm" class="form-panel">
          <span class="close-button" @click="closeform">&times;</span>
          <h2>Add New Task</h2>
          <form @submit.prevent="submitForm">
            <label>Hari:</label>
            <select v-model="form.hari" required>
              <option value="Senin">Monday</option>
              <option value="Selasa">Tuesday</option>
              <option value="Rabu">Wednesday</option>
              <option value="Kamis">Thursday</option>
              <option value="Jumat">Friday</option>
              <option value="Sabtu">Saturday</option>
              <option value="Minggu">Sunday</option>
            </select>
    
            <label>Judul:</label>
            <input type="text" v-model="form.judul" required />
    
            <label>Tanggal:</label>
            <input type="date" v-model="form.date" required />
    
            <label>Kategori:</label>
            <select v-model="form.Kategori" required>
                <option value="Important">Important</option>
                <option value="Urgent">Urgent</option>
                <option value="Reguler">Reguler</option>
            </select>
    
            <label>Deskripsi:</label>
            <textarea v-model="form.deskripsi" required></textarea>
            
            <div class="submit-container">
              <button type="submit" id="send-task">Add</button>
            </div>
          </form>
        </div>
      </transition>

      <transition name="slide">
        <div v-if="showForm1" class="form-panel">
          <span class="close-button" @click="closeform1">&times;</span>
          <h2>Edit Task</h2>
          <form @submit.prevent="submitForm1" >
            <label>Hari:</label>
            <select v-model="form1.hari" required>
              <option value="Senin">Monday</option>
              <option value="Selasa">Tuesday</option>
              <option value="Rabu">Wednesday</option>
              <option value="Kamis">Thursday</option>
              <option value="Jumat">Friday</option>
              <option value="Sabtu">Saturday</option>
              <option value="Minggu">Sunday</option>
            </select>
    
            <label>Judul:</label>
            <input type="text" v-model="form1.judul" required />
    
            <label>Tanggal:</label>
            <input type="date" v-model="form1.date" required />
    
            <label>Kategori:</label>
            <select v-model="form1.Kategori" required>
                <option value="Important">Important</option>
                <option value="Urgent">Urgent</option>
                <option value="Reguler">Reguler</option>
            </select>
    
            <label>Deskripsi:</label>
            <textarea v-model="form1.deskripsi" required></textarea>
            <div class="edit-button-container">
              <button type="button" @click="markAsDone(this.editingTaskId)" id="mark-done-task">Mark Done!</button>
              <div class="save-delete-button">
                <button type="submit" id="send-task">Save</button>
                <button type="button" @click="deleteTask(this.editingTaskId)" id="delete-task">delete</button>
              </div>
            </div>
            </form>
            
          
        </div>
      </transition>
      <br />

      <div class="schedules">
        <div class="schedule-table">
          <h3>MONDAY</h3>
          <hr id="day-separator" />
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Senin')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
      
        <div class="schedule-table">
          <h3>TUESDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Selasa')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
        
        <div class="schedule-table">
          <h3>WEDNESDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Rabu')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
      
        <div class="schedule-table">
          <h3>THURSDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Kamis')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
    
        <div class="schedule-table">
          <h3>FRIDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li
              v-for="post in filteredPostsByDay('Jumat')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>

        <div class="schedule-table">
          <h3>SATURDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Sabtu')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
    
        <div class="schedule-table">
          <h3>SUNDAY</h3>
          <hr id="day-separator"/>
          <ul>
            <li 
              v-for="post in filteredPostsByDay('Minggu')"
              :key="post.id"
              :class="['task-box', getKategoriClass(post.Kategori,post.status)]"
            >
              <span 
              :id="post.Kategori === 'Done' ? null : 'dates'"
              :class="{ 'text-done': post.Kategori === 'Done' }"> 
                {{ formatDate(post.date) }} 
              </span> 
              <strong
                :id="Object.keys(getKategoriClass(post.Kategori,post.status)).find(key => getKategoriClass(post.Kategori,post.status)[key]) + '-task'"
              >
              {{ post.judul }}
              </strong>
              <br />
              <p :class="[{ 'description-done': post.Kategori === 'Done' }]">
                {{ post.deskripsi }}
              </p>
              <button id="edit-task" v-if="post.status !== 'Done'" @click="startEditing(post) ">Edit Task!</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>

template {
  margin: 0px;
  /* background-color: #f2fffa;  */
}

* {
  font-family: Arial, Helvetica, sans-serif;
  /* background-color: #f2fffa;  */
}

body {
  /* background-color: #f2fffa; */
  margin: 0;
}

.dashboard-page {
  /* background-color: #f2fffa;  */
  margin: 0px;
  padding: 0px;
}

h3 {
  color: #102542;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* background-color: #f2fffa; */
  padding: 10px;
}

button:active {
  background-color: #102542;
  color: white;
}

#add-task {
  width: 40px;
  height: 40px;
  padding: 0;
  text-align: center;
  background-color: #379634;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: larger;
}

#add-task:active {
  background-color: #102542;
  color: white;
}

#send-task {
  padding: 10px;
  border-radius: 5px;
  background-color: #379634;
  color: white;
  border: none;
  cursor: pointer;
  width: auto;
  float: right;
  margin-top: 10px;
}

#send-task:active {
  background-color: #102542;
  color: white;
}

#mark-done-task {
  padding: 10px;
  border-radius: 5px;
  background: transparent;
  color: #379634;
  border: 2px solid #379634;
  cursor: pointer;
  width: auto;
  float: right;
  margin-top: 10px;
}

#mark-done-task:active {
  border-color: #102542;
  color: #102542;
}

#edit-task {
  padding: 10px;
  border-radius: 5px;
  background: transparent;
  color: #379634;
  border: 2px solid #379634;
  cursor: pointer;
  width: auto;
  margin-top: 10px;
}

#edit-task:hover {
  background-color: #c2ffe7;
}

#edit-task:active {
  border-color: #102542;
  color: #102542;
}

#delete-task {
  padding: 10px;
  border-radius: 5px;
  background-color: #db162f;
  color: white;
  border: none;
  cursor: pointer;
  width: auto;
  float: right;
  margin-top: 10px;
}

.submit-container {
  display: flex;
  justify-content: flex-end;
}

.save-delete-button {
  display: flex;
  gap: 20px;
}

.edit-button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* memunculkan form di panel sebelah kanan: */
.form-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 30%; 
  height: 100%;
  /* background-color: #eefaf4; */
  background-color: #f2fffa;
  border-radius: 10px;
  box-shadow: -2px 0 10px rgba(0,0,0,0.1);
  padding: 30px;
  z-index: 1000;
  overflow-y: auto;
  transition: transform 0.3s ease-in-out;
}

/* Transisi slide-in dari kanan */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from, .slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.slide-enter-to, .slide-leave-from {
  transform: translateX(0%);
  opacity: 1;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 24px;
  font-weight: bold;
  /* color: #333; */
  color: #379634;
  cursor: pointer;
}

.close-button:active {
  color: #102542;
}

.form-panel h2 {
  margin-bottom: 20px;
  color: #102542;
}

.form-panel form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-panel label {
  color: #102542;
  font-weight: bold;
  margin-top: 10px;
  margin-bottom: 2px;
}

.form-panel input,
.form-panel select,
.form-panel textarea {
  padding: 8px;
  border: 1px solid #ccc;
  background-color: #f2fffa;
  border-radius: 6px;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}

.form-panel textarea {
  resize: vertical;
  min-height: 80px;
}

.dashboard-page {
  padding: 30px;
}

.filter-container {
  display: flex;
  gap: 40px;
}

.filter-container label {
  font-weight: bold;
}

#important-task {
  color: #d9534f;
}

#urgent-task {
  color: #0275d8;
}

#reguler-task {
  color: #f0ad4e;
}

#dates {
  font-size: smaller;
  font-weight: bold;
  color: #102542; 
  display: block;
  margin-bottom: 10px;
}

/* untuk task yang ditandai selesai: */
#done-task {
  color: #bebebe;
}

.text-done {
  font-size: smaller;
  font-weight: bold;
  color: #bebebe;
  display: block;
  margin-bottom: 10px;
}

.dates {
  color: #bebebe;
}

.description-done {
  color: #bebebe;
}

.schedules {
  display: flex;
}

.schedule-table {
  border: 1px solid #74f2ce;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  width: 100%;
  min-height: 300px;
}

.schedule-table ul {
  list-style-type: none; 
  padding-left: 0;      
  margin-bottom: 20px;
}

.schedule-table li {
  margin-bottom: 20px;
}

#day-separator {
  border: 1px solid #74f2ce;
  width: 100%;
}

.important {
  border: 3px solid #d9534f;
  border-radius: 4%;
  padding: 20px;
}

.urgent {
  border: 3px solid #0275d8;
  border-radius: 4%;
  padding: 20px;
}

.reguler {
  border: 3px solid #f0ad4e;
  border-radius: 4%;
  padding: 20px;
}

.done {
  border: 3px solid #d9d9d9;
  border-radius: 4%;
  padding: 20px;
}

/* tampilan mobile: */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
  }

  .filter-container {
    flex-wrap: wrap;
    gap: 20px;
    justify-content: flex-start;
  }

  #add-task {
    /* width: 100%; */
    margin-top: 20px;
    width: 40px;
    height: 40px;
  }

  .form-panel {
    /* width: 100vw; */
    width: 300px;
    height: 100%;
    padding: 20px 20px;
    border-radius: 0;
    box-shadow: none;
    position: fixed;
    top: 0;
    right: 0;
    overflow-y: auto;
    z-index: 1000;
    background-color: #f2fffa;
  }

  .form-panel h2 {
    font-size: 20px;
  }

  .form-panel label {
    font-size: 14px;
  }

  .form-panel input,
  .form-panel select,
  .form-panel textarea {
    font-size: 16px;
  }

  .form-panel textarea {
    resize: vertical;
    min-height: 60px;
  }

  .submit-container {
    margin-top: 0px;
    justify-content: center;
  }

  .close-button {
    font-size: 28px;
    top: 10px;
    right: 10px;
  }

  .schedules {
    flex-direction: column;
  }

  .schedule-table {
    width: 100%;
    padding: 10px 0px;
    margin-bottom: 20px;
  }

  .task-box {
    font-size: 14px;
  }

  .form-panel input,
  .form-panel select,
  .form-panel textarea {
    font-size: 16px;
  }
}

</style>

