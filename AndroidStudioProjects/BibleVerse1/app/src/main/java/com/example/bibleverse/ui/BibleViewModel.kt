package com.example.bibleverse.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.asLiveData
import androidx.lifecycle.viewModelScope
import com.example.bibleverse.data.AppDatabase
import com.example.bibleverse.data.JournalEntry
import com.example.bibleverse.model.DayReading
import com.example.bibleverse.repository.BibleRepository
import kotlinx.coroutines.launch

class BibleViewModel(application: Application) : AndroidViewModel(application) {

    private val repository: BibleRepository
    val allJournals: LiveData<List<JournalEntry>>

    private val _currentDay = MutableLiveData(42)
    val currentDay: LiveData<Int> = _currentDay

    private val _isOneYearPlan = MutableLiveData(true)
    val isOneYearPlan: LiveData<Boolean> = _isOneYearPlan

    private val _todayReading = MutableLiveData<DayReading>()
    val todayReading: LiveData<DayReading> = _todayReading

    init {
        val journalDao = AppDatabase.getDatabase(application).journalDao()
        repository = BibleRepository(journalDao)
        allJournals = repository.allJournals.asLiveData()
        loadTodayReading()
    }

    private fun loadTodayReading() {
        _todayReading.value = repository.getReadingForDay(_currentDay.value ?: 1, _isOneYearPlan.value ?: true)
    }

    fun saveJournal(book: String, chapter: Int, content: String) {
        viewModelScope.launch {
            val entry = JournalEntry(book = book, chapter = chapter, content = content)
            repository.saveJournal(entry)
        }
    }

    fun deleteJournal(journal: JournalEntry) {
        viewModelScope.launch {
            repository.deleteJournal(journal)
        }
    }

    fun searchJournals(query: String): LiveData<List<JournalEntry>> {
        return repository.searchJournals(query).asLiveData()
    }

    fun exportJournals(): String {
        // Simple JSON-like export for demo
        val journals = allJournals.value ?: return "[]"
        val sb = StringBuilder()
        sb.append("[\n")
        journals.forEachIndexed { index, entry ->
            sb.append("  {\n")
            sb.append("    \"book\": \"${entry.book}\",\n")
            sb.append("    \"chapter\": ${entry.chapter},\n")
            sb.append("    \"content\": \"${entry.content.replace("\n", "\\n")}\",\n")
            sb.append("    \"date\": ${entry.date}\n")
            sb.append("  }${if (index < journals.size - 1) "," else ""}\n")
        }
        sb.append("]")
        return sb.toString()
    }

    fun importJournals(json: String) {
        // Basic simulation of import
        viewModelScope.launch {
            // In a real app, use a JSON parser like GSON or Kotlin Serialization
            Toast.makeText(getApplication(), "Importing data...", Toast.LENGTH_SHORT).show()
        }
    }
}
import android.widget.Toast
