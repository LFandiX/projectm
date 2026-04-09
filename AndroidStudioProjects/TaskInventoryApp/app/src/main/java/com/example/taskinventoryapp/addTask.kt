package com.example.taskinventoryapp

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.Toast
import androidx.navigation.fragment.findNavController
import com.example.taskinventory.api.RetrofitClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class addTask : Fragment() {

    private lateinit var inTitle : EditText
    private lateinit var inDesc : EditText
    private lateinit var inCategory : RadioGroup
    private lateinit var addBtn : Button



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {

        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_add_task, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        inTitle = view.findViewById(R.id.etTitle)
        inDesc = view.findViewById(R.id.etDescription)
        inCategory = view.findViewById(R.id.rgCategory)
        addBtn = view.findViewById(R.id.btnSaveTask)
        val backBtn = view.findViewById<ImageButton>(R.id.btnBack)
        backBtn.setOnClickListener {
            findNavController().popBackStack()
        }
        addBtn.setOnClickListener {
            addtask()
        }

    }

    private fun addtask() {
        val titleVal = inTitle.text.toString().trim()
        val descVal = inDesc.text.toString().trim()

        if (titleVal.isEmpty()) {
            inTitle.error = "Judul wajib diisi"
            return
        }

        val selectedId = inCategory.checkedRadioButtonId
        val categoryCode = when (selectedId) {
            R.id.rbUrgent -> "U"
            R.id.rbImportant -> "I"
            else -> "N" // Default Normal
        }
//        Toast.makeText(context, "${titleVal} ${descVal} ${categoryCode}", Toast.LENGTH_SHORT).show()
        val call = RetrofitClient.instance.createTask(titleVal,descVal,categoryCode)
        call.enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Task Berhasil Dibuat!", Toast.LENGTH_SHORT).show()

                    // Kembali ke Halaman Utama
                    findNavController().popBackStack()
                } else {
                    Toast.makeText(context, "Gagal: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                if (context != null) {
                    Toast.makeText(context, "Error Koneksi", Toast.LENGTH_SHORT).show()
                    Log.e("AddTaskFragment", "Error: ${t.message}")
                }
            }
        })

    }

}