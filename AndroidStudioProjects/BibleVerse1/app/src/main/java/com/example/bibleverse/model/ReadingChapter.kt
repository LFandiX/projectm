package com.example.bibleverse.model

data class ReadingChapter(
    val book: String,
    val chapter: Int,
    val context: String,
    val exposition: String
)
