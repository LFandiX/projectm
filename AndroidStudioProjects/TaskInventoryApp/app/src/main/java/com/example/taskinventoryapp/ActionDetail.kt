package com.example.taskinventoryapp

import android.graphics.Color
import android.os.AsyncTask
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.navigation.fragment.findNavController
import com.example.taskinventory.api.RetrofitClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ActionDetail : Fragment() {
    private lateinit var DetailTitle : TextView
    private lateinit var DetailDesc : TextView
    private lateinit var DetailCat : TextView
    private lateinit var DetailStatus : TextView

    private lateinit var DetailBtn : Button

    private var id : Int = 0
    private var status : String = ""
    private var nextStatus : String = ""




    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {

        }
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?,
                              savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_action_detail, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        DetailTitle = view.findViewById(R.id.tvDetailTitle)
        DetailDesc = view.findViewById(R.id.tvDetailDesc)
        DetailCat = view.findViewById(R.id.tvDetailCategory)
        DetailStatus = view.findViewById(R.id.tvDetailStatus)
        DetailBtn = view.findViewById(R.id.btnProcessAction)

        val backBtn = view.findViewById<ImageButton>(R.id.btnBack)
        backBtn.setOnClickListener {
            findNavController().popBackStack()
        }
        arguments?.let {
            id = it.getInt("ARG_ID")
            val title = it.getString("ARG_TITLE")
            val desc = it.getString("ARG_DESC")
            val category = it.getString("ARG_CATEGORY")
            status = it.getString("ARG_STATUS") ?: "New"

            if (category == "I") {
                DetailCat.text  = "Important"
                DetailCat.setBackgroundColor(Color.rgb(255, 165, 0))
            } else if (category == "U") {
                DetailCat.text = "Urgent"
                DetailCat.setBackgroundColor(Color.RED)
            } else {
                DetailCat.text = "Normal"
                DetailCat.setBackgroundColor(Color.BLUE)
            }
            DetailTitle.text = title
            DetailDesc.text = desc ?: "No Description"
            DetailStatus.text = "Current Status: $status"

        }

        setupDetailBtn()
        DetailBtn.setOnClickListener {
            saveToAPI()
        }


    }
    private fun setupDetailBtn() {
        if (status == "New") {
            DetailBtn.text = "TAKE TASK"
            nextStatus = "In Progress"

        } else if (status == "In Progress") {
            DetailBtn.text = "MARK AS DONE"
            nextStatus = "Done"

        } else {
            DetailBtn.visibility = View.GONE
        }
    }

    private fun saveToAPI() {
        val call = RetrofitClient.instance.updateTaskStatus(id,nextStatus)

        call.enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(context, "Berhasil update ke: $nextStatus", Toast.LENGTH_SHORT).show()

                    findNavController().popBackStack()
                } else {
                    Toast.makeText(context, "Gagal Update: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                if (context != null) {
                    Toast.makeText(context, "Error Koneksi Internet", Toast.LENGTH_SHORT).show()
                    Log.e("ActionDetail", "Error: ${t.message}")
                }
            }
        })
    }

}