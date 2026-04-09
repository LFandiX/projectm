package com.example.bibleverse.ui

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.bibleverse.R
import com.example.bibleverse.databinding.FragmentHistoryBinding
import com.example.bibleverse.ui.adapter.HistoryAdapter

class HistoryFragment : Fragment() {
    private var _binding: FragmentHistoryBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BibleViewModel by viewModels()
    private lateinit var adapter: HistoryAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHistoryBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState: Bundle?)

        adapter = HistoryAdapter(
            onDelete = { entry -> viewModel.deleteJournal(entry) },
            onView = { entry ->
                val bundle = Bundle().apply {
                    putString("book", entry.book)
                    putInt("chapter", entry.chapter)
                }
                findNavController().navigate(R.id.action_historyFragment_to_journalFragment, bundle)
            }
        )

        binding.historyRecycler.adapter = adapter
        binding.historyRecycler.layoutManager = LinearLayoutManager(context)

        viewModel.allJournals.observe(viewLifecycleOwner) { journals ->
            adapter.submitList(journals)
        }

        binding.searchInput.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                val query = s.toString()
                if (query.isNotEmpty()) {
                    viewModel.searchJournals(query).observe(viewLifecycleOwner) { filtered ->
                        adapter.submitList(filtered)
                    }
                } else {
                    viewModel.allJournals.observe(viewLifecycleOwner) { journals ->
                        adapter.submitList(journals)
                    }
                }
            }
            override fun afterTextChanged(s: Editable?) {}
        })
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
