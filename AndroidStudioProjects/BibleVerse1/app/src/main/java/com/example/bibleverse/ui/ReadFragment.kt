package com.example.bibleverse.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import com.example.bibleverse.R
import com.example.bibleverse.databinding.FragmentReadBinding

class ReadFragment : Fragment() {
    private var _binding: FragmentReadBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BibleViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentReadBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState: Bundle?)

        val book = arguments?.getString("book") ?: ""
        val chapter = arguments?.getInt("chapter") ?: 1
        val context = arguments?.getString("context") ?: ""
        val exposition = arguments?.getString("exposition") ?: ""

        binding.bookName.text = book
        binding.chapterNumber.text = "Chapter $chapter"
        binding.contextText.text = context
        binding.expositionText.text = exposition

        viewModel.allJournals.observe(viewLifecycleOwner) { journals ->
            val hasJournal = journals.any { it.book == book && it.chapter == chapter }
            if (hasJournal) {
                binding.btnJournal.text = "View/Edit Journal"
                binding.btnJournal.setBackgroundColor(requireContext().getColor(R.color.green_700))
                binding.btnJournal.setIconResource(R.drawable.ic_check_circle)
            } else {
                binding.btnJournal.text = "Write Journal"
                binding.btnJournal.setBackgroundColor(requireContext().getColor(R.color.blue_900))
                binding.btnJournal.setIconResource(R.drawable.ic_pen_line)
            }
        }

        binding.btnBack.setOnClickListener {
            findNavController().navigateUp()
        }

        binding.btnJournal.setOnClickListener {
            val bundle = Bundle().apply {
                putString("book", book)
                putInt("chapter", chapter)
            }
            findNavController().navigate(R.id.action_readFragment_to_journalFragment, bundle)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
