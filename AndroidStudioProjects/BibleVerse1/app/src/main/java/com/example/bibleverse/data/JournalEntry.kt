package com.example.bibleverse.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "journals")
data class JournalEntry(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val book: String,
    val chapter: Int,
    val content: String,
    val date: Long = System.currentTimeMillis()
)
