package com.example.bibleverse.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.bibleverse.R
import com.example.bibleverse.databinding.FragmentDashboardBinding
import com.example.bibleverse.ui.adapter.ReadingAdapter
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class DashboardFragment : Fragment() {

    private var _binding: FragmentDashboardBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BibleViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState: Bundle?)

        val sdf = SimpleDateFormat("EEEE, MMMM dd, yyyy", Locale.ENGLISH)
        binding.currentDate.text = sdf.format(Date())

        viewModel.currentDay.observe(viewLifecycleOwner) { day ->
            binding.dayCounter.text = "Day $day"
        }

        viewModel.isOneYearPlan.observe(viewLifecycleOwner) { isOneYear ->
            binding.readingMode.text = if (isOneYear) "Mode: 1 Year Plan" else "Mode: 1 Chapter per Day"
        }

        viewModel.allJournals.observe(viewLifecycleOwner) { journals ->
            val journaledKeys = journals.map { "${it.book}_${it.chapter}" }.toSet()
            updateReadingList(journaledKeys)
            
            // Simplified streak calculation for demo
            binding.streakNumber.text = "${journals.size} Days Logged"
            
            val totalChapters = 1189 // Total Bible chapters
            val progress = (journals.size * 100) / totalChapters
            binding.overallProgress.progress = progress
            binding.progressPercent.text = "$progress% Complete"
            binding.days_left.text = "${365 - journals.size} days left"
        }

        binding.btnHistory.setOnClickListener {
            findNavController().navigate(R.id.action_dashboardFragment_to_historyFragment)
        }

        binding.btnSettings.setOnClickListener {
            findNavController().navigate(R.id.action_dashboardFragment_to_settingsFragment)
        }
    }

    private fun updateReadingList(journaledKeys: Set<String>) {
        viewModel.todayReading.observe(viewLifecycleOwner) { dayReading ->
            val adapter = ReadingAdapter(dayReading.chapters, journaledKeys) { chapter ->
                val bundle = Bundle().apply {
                    putString("book", chapter.book)
                    putInt("chapter", chapter.chapter)
                    putString("context", chapter.context)
                    putString("exposition", chapter.exposition)
                }
                findNavController().navigate(R.id.action_dashboardFragment_to_readFragment, bundle)
            }
            binding.readingRecycler.layoutManager = LinearLayoutManager(context)
            binding.readingRecycler.adapter = adapter
            
            val count = dayReading.chapters.count { journaledKeys.contains("${it.book}_${it.chapter}") }
            binding.journaledStatus.text = "$count of ${dayReading.chapters.size} journaled"
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
