package com.example.bibleverse.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface JournalDao {
    @Query("SELECT * FROM journals ORDER BY date DESC")
    fun getAllJournals(): Flow<List<JournalEntry>>

    @Query("SELECT * FROM journals WHERE book = :book AND chapter = :chapter LIMIT 1")
    suspend fun getJournalByChapter(book: String, chapter: Int): JournalEntry?

    @Query("SELECT * FROM journals WHERE book LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%'")
    fun searchJournals(query: String): Flow<List<JournalEntry>>

    @Query("SELECT * FROM journals WHERE book = :book")
    fun getJournalsByBook(book: String): Flow<List<JournalEntry>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertJournal(journal: JournalEntry)

    @Delete
    suspend fun deleteJournal(journal: JournalEntry)
}
