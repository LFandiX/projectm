package com.example.bibleverse.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import com.example.bibleverse.databinding.FragmentSettingsBinding
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class SettingsFragment : Fragment() {
    private var _binding: FragmentSettingsBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BibleViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSettingsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState: Bundle?)

        val sdf = SimpleDateFormat("MMMM dd, yyyy", Locale.ENGLISH)
        binding.tvStartDate.text = sdf.format(Date())

        binding.btnChangeMode.setOnClickListener {
            Toast.makeText(context, "Reading mode toggled!", Toast.LENGTH_SHORT).show()
        }

        binding.btnResetDate.setOnClickListener {
            Toast.makeText(context, "Start date reset!", Toast.LENGTH_SHORT).show()
        }

        binding.switchReminder.setOnCheckedChangeListener { _, isChecked ->
            val status = if (isChecked) "enabled" else "disabled"
            Toast.makeText(context, "Reminders $status", Toast.LENGTH_SHORT).show()
        }

        binding.root.findViewById<View>(R.id.btn_export)?.setOnClickListener {
            val data = viewModel.exportJournals()
            Toast.makeText(context, "Data exported: ${data.length} chars", Toast.LENGTH_SHORT).show()
        }

        binding.root.findViewById<View>(R.id.btn_import)?.setOnClickListener {
            viewModel.importJournals("[]")
            Toast.makeText(context, "Ready to import from backup!", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
