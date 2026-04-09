package com.example.uas

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.uas.api.RetrofitClient
import com.example.uas.model.TaskRequest
import kotlinx.coroutines.launch

class AddTaskFragment : Fragment() {

    private lateinit var etTitle: EditText
    private lateinit var etDescription: EditText
    private lateinit var spinnerCategory: Spinner
    private lateinit var spinnerStatus: Spinner
    private lateinit var btnSave: Button
    private lateinit var btnCancel: Button
    private lateinit var progressBar: ProgressBar

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(R.layout.fragment_add_task, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        initViews(view)
        setupSpinners()
        setupButtons()
    }

    private fun initViews(view: View) {
        etTitle = view.findViewById(R.id.etTitle)
        etDescription = view.findViewById(R.id.etDescription)
        spinnerCategory = view.findViewById(R.id.spinnerCategory)
        spinnerStatus = view.findViewById(R.id.spinnerStatus)
        btnSave = view.findViewById(R.id.btnSave)
        btnCancel = view.findViewById(R.id.btnCancel)
        progressBar = view.findViewById(R.id.progressBar)
    }

    private fun setupSpinners() {
        val categories = arrayOf("Normal (N)", "Urgent (U)", "Important (I)")
        spinnerCategory.adapter = ArrayAdapter(
            requireContext(),
            android.R.layout.simple_spinner_item,
            categories
        ).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }

        val statuses = arrayOf("New", "In Progress", "Done")
        spinnerStatus.adapter = ArrayAdapter(
            requireContext(),
            android.R.layout.simple_spinner_item,
            statuses
        ).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }
    }

    private fun setupButtons() {
        btnSave.setOnClickListener { saveTask() }
        btnCancel.setOnClickListener {
            findNavController().navigateUp()
        }
    }

    private fun saveTask() {
        val title = etTitle.text.toString().trim()
        val description = etDescription.text.toString().trim()

        if (title.isEmpty()) {
            etTitle.error = "Title is required"
            return
        }

        val category = when (spinnerCategory.selectedItemPosition) {
            0 -> "N"
            1 -> "U"
            2 -> "I"
            else -> "N"
        }

        val status = spinnerStatus.selectedItem.toString()

        val task = TaskRequest(title, description, category, status)
        addTaskToServer(task)
    }

    private fun addTaskToServer(task: TaskRequest) {
        showLoading(true)

        lifecycleScope.launch {
            try {
                val response = RetrofitClient.instance.createTask(task)
                showLoading(false)

                if (response.isSuccessful && response.body()?.success == true) {
                    Toast.makeText(requireContext(), "Task added!", Toast.LENGTH_SHORT).show()
                    findNavController().navigateUp()
                } else {
                    Toast.makeText(
                        requireContext(),
                        response.body()?.message ?: "Failed",
                        Toast.LENGTH_LONG
                    ).show()
                }
            } catch (e: Exception) {
                showLoading(false)
                Toast.makeText(requireContext(), e.message, Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun showLoading(isLoading: Boolean) {
        progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
        btnSave.isEnabled = !isLoading
        btnCancel.isEnabled = !isLoading
    }
}
