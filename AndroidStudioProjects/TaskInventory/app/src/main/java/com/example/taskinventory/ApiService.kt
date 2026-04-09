package com.example.taskinventory.api


// import Allneeded
import com.example.taskinventory.model.Task
import retrofit2.Response
import retrofit2.http.GET

interface ApiService {
    @GET("api/tasks") // Sesuaikan dengan route di Flask kamu (misal: @app.route('/tasks'))
    suspend fun getAllTasks(): Response<List<Task>>
}