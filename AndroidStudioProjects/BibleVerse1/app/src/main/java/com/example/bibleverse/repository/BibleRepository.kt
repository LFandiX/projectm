package com.example.bibleverse.repository

import com.example.bibleverse.data.JournalDao
import com.example.bibleverse.data.JournalEntry
import com.example.bibleverse.model.DayReading
import com.example.bibleverse.model.ReadingChapter
import kotlinx.coroutines.flow.Flow

class BibleRepository(private val journalDao: JournalDao) {

    val allJournals: Flow<List<JournalEntry>> = journalDao.getAllJournals()

    suspend fun getJournal(book: String, chapter: Int): JournalEntry? {
        return journalDao.getJournalByChapter(book, chapter)
    }

    suspend fun saveJournal(journal: JournalEntry) {
        journalDao.insertJournal(journal)
    }

    suspend fun deleteJournal(journal: JournalEntry) {
        journalDao.deleteJournal(journal)
    }

    fun searchJournals(query: String): Flow<List<JournalEntry>> {
        return journalDao.searchJournals(query)
    }

    fun getJournalsByBook(book: String): Flow<List<JournalEntry>> {
        return journalDao.getJournalsByBook(book)
    }

    // This would ideally come from a JSON file in assets
    fun getReadingForDay(day: Int, isOneYearPlan: Boolean): DayReading {
        // Mock data for Day 1
        return if (isOneYearPlan) {
            DayReading(
                day = day,
                chapters = listOf(
                    ReadingChapter("Genesis", 1, "Context for Gen 1...", "Exposition for Gen 1..."),
                    ReadingChapter("Genesis", 2, "Context for Gen 2...", "Exposition for Gen 2..."),
                    ReadingChapter("Matthew", 1, "Context for Mat 1...", "Exposition for Mat 1..."),
                    ReadingChapter("Psalms", 1, "Context for Psa 1...", "Exposition for Psa 1...")
                )
            )
        } else {
            DayReading(
                day = day,
                chapters = listOf(
                    ReadingChapter("Genesis", day, "Context for Gen $day...", "Exposition for Gen $day...")
                )
            )
        }
    }
}
