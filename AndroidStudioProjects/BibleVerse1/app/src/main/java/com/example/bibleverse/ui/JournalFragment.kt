package com.example.bibleverse.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.bibleverse.data.AppDatabase
import com.example.bibleverse.databinding.FragmentJournalBinding
import kotlinx.coroutines.launch

class JournalFragment : Fragment() {
    private var _binding: FragmentJournalBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BibleViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentJournalBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState: Bundle?)

        val book = arguments?.getString("book") ?: ""
        val chapter = arguments?.getInt("chapter") ?: 1

        binding.bookChapter.text = "$book $chapter"

        // Check for existing journal
        val db = AppDatabase.getDatabase(requireContext())
        lifecycleScope.launch {
            val existing = db.journalDao().getJournalByChapter(book, chapter)
            existing?.let {
                binding.journalInput.setText(it.content)
            }
        }

        binding.btnBack.setOnClickListener {
            findNavController().navigateUp()
        }

        binding.btnSave.setOnClickListener {
            val content = binding.journalInput.text.toString()
            if (content.isNotBlank()) {
                viewModel.saveJournal(book, chapter, content)
                Toast.makeText(context, "Journal saved!", Toast.LENGTH_SHORT).show()
                findNavController().navigateUp()
            } else {
                Toast.makeText(context, "Please write something first.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
