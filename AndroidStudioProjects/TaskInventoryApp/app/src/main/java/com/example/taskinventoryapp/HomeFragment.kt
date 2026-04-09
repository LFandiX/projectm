package com.example.taskinventoryapp

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.navigation.fragment.findNavController
import androidx.navigationevent.findViewTreeNavigationEventDispatcherOwner
import com.example.taskinventory.api.RetrofitClient
import com.example.taskinventory.model.Task
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response



class HomeFragment : Fragment() {
    private lateinit var CountNew: TextView
    private lateinit var CountInProgress: TextView
    private lateinit var CountDone: TextView

    private lateinit var boxNew: LinearLayout
    private lateinit var boxInProgress: LinearLayout
    private lateinit var boxDone: LinearLayout
    private lateinit var btnAddTask: ImageButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        CountNew = view.findViewById<TextView>(R.id.tvCountNew)
        CountInProgress = view.findViewById<TextView>(R.id.tvCountInProgress)
        CountDone = view.findViewById<TextView>(R.id.tvCountDone)

        boxNew = view.findViewById<LinearLayout>(R.id.boxNew)
        boxInProgress = view.findViewById<LinearLayout>(R.id.boxInProgress)
        boxDone = view.findViewById<LinearLayout>(R.id.boxDone)

        btnAddTask = view.findViewById<ImageButton>(R.id.btnAddTask)

        loadAPI()

        setupNavigation()
    }

    private fun loadAPI() {
        val call = RetrofitClient.instance.getAllTasks()
        call.enqueue(object : Callback<List<Task>>{
            override fun onResponse(
                call: Call<List<Task>?>,
                response: Response<List<Task>?>
            ) {
                if (response.isSuccessful){
                    val tasks = response.body() ?: emptyList()
                    val CountNewVal = tasks.count { it.status == "New" && it.deleted == "False" }
                    val CountInProgressVal = tasks.count { it.status == "In Progress" && it.deleted == "False" }
                    val CountDoneVal = tasks.count { it.status == "Done" && it.deleted == "False" }

                    CountNew.text = CountNewVal.toString()
                    CountInProgress.text = CountInProgressVal.toString()
                    CountDone.text = CountDoneVal.toString()
                }
                else {
                    Toast.makeText(context, "Gagal Mengambil Data", Toast.LENGTH_SHORT).show()
                }

            }

            override fun onFailure(
                call: Call<List<Task>?>,
                t: Throwable
            ) {
                Log.e("HomeFragment", "Error: ${t.message}")
                if (context != null) {
                    Toast.makeText(context, "Koneksi Error", Toast.LENGTH_SHORT).show()
                }
            }
        })
    }

    private fun setupNavigation() {
        boxNew.setOnClickListener {
            val Bundle = Bundle()
            Bundle.putString("STATUS_FILTER", "New")
            findNavController().navigate(R.id.action_homeFragment_to_taskDetail,Bundle)
        }
        boxInProgress.setOnClickListener {
            val Bundle = Bundle()
            Bundle.putString("STATUS_FILTER", "In Progress")
            findNavController().navigate(R.id.action_homeFragment_to_taskDetail,Bundle)
        }
        boxDone.setOnClickListener {
            val Bundle = Bundle()
            Bundle.putString("STATUS_FILTER", "Done")
            findNavController().navigate(R.id.action_homeFragment_to_taskDetail,Bundle)
        }
        btnAddTask.setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_addTask)
        }
    }
}













