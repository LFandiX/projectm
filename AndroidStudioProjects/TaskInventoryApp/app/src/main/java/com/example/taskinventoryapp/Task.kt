package com.example.taskinventory.model

import com.google.gson.annotations.SerializedName

data class Task(
    val id: Int,
    val title: String,
    val description: String?,
    val category: String, // 'N', 'U', 'I'
    val status: String,   // 'New', 'In Progress', 'Done'

    @SerializedName("created_time")
    val createdTime: String?,

    @SerializedName("finished_time")
    val finishedTime: String?,

    val duration: Int?,
    val deleted: String // 'False', 'True'
)