package com.example.uas

import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import com.example.uas.api.RetrofitClient
import com.example.uas.model.Task
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController

class TaskDetail : Fragment() {
    private lateinit var lvTaskList: ListView
    private lateinit var tvPageTitle: TextView
    private lateinit var btnFilterN: Button
    private lateinit var btnFilterU: Button
    private lateinit var btnFilterI: Button

    private lateinit var btnBack: Button

    private lateinit var adapter: SimpleTaskAdapter
    private var allTasks: List<Task> = listOf()


    private var currentStatusFilter = "New"
    private var currentCategoryFilter = "All"
    private var dataSudahDiload = false


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_task_detail, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        lvTaskList = view.findViewById(R.id.lvTaskList)
        tvPageTitle = view.findViewById(R.id.tvPageTitle)
        btnFilterN = view.findViewById(R.id.btnFilterN)
        btnFilterU = view.findViewById(R.id.btnFilterU)
        btnFilterI = view.findViewById(R.id.btnFilterI)
        btnBack = view.findViewById(R.id.btnBack)

        arguments?.let {
            currentStatusFilter = it.getString("STATUS_FILTER", "New")
        }
        tvPageTitle.text = "$currentStatusFilter Tasks"

        adapter = SimpleTaskAdapter(requireContext())
        lvTaskList.adapter = adapter

        loadDataDariServer()

        btnFilterN.setOnClickListener { currentCategoryFilter = "N"; saringData() }
        btnFilterU.setOnClickListener { currentCategoryFilter = "U"; saringData() }
        btnFilterI.setOnClickListener { currentCategoryFilter = "I"; saringData() }

        btnBack.setOnClickListener {
            findNavController().navigate(R.id.homeFragment)
        }
    }

    private fun loadDataDariServer() {
        val call = RetrofitClient.instance.getAllTasks()
        call.enqueue(object : Callback<List<Task>> {
            override fun onResponse(call: Call<List<Task>>, response: Response<List<Task>>) {
                if (response.isSuccessful) {
                    allTasks = response.body() ?: emptyList()
                    saringData()
                }
            }
            override fun onFailure(call: Call<List<Task>>, t: Throwable) {
                if(context != null) Toast.makeText(context, "Error Koneksi", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun saringData() {
        val hasilSaringan = allTasks.filter { task ->
            val statusCocok = task.status == currentStatusFilter && task.deleted == "False"
            val kategoriCocok = if (currentCategoryFilter == "All") true else task.category == currentCategoryFilter
            statusCocok && kategoriCocok
        }
        adapter.isiData(hasilSaringan)
    }

    inner class SimpleTaskAdapter(private val context: Context) : BaseAdapter() {

        var listData: List<Task> = ArrayList()

        fun isiData(dataBaru: List<Task>) {
            listData = dataBaru
            notifyDataSetChanged()
        }

        override fun getCount(): Int = listData.size
        override fun getItem(position: Int): Any = listData[position]
        override fun getItemId(position: Int): Long = position.toLong()

        override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
            var view = convertView
            if (view == null) {
                view = LayoutInflater.from(context).inflate(R.layout.item_task, parent, false)
            }

            val task = listData[position]

            val tvTitle = view!!.findViewById<TextView>(R.id.tvTaskTitle)
            val tvTime = view.findViewById<TextView>(R.id.tvTaskTime)
            val tvBadge = view.findViewById<TextView>(R.id.tvCategoryBadge)
            val btnAction = view.findViewById<Button>(R.id.btnAction)
            val tvDuration = view.findViewById<TextView>(R.id.tvDuration)

            // Isi Datanya
            tvTitle.text = task.title
            tvTime.text = task.createdTime

            if (task.category == "U") {
                tvBadge.text = "URGENT"
                tvBadge.setBackgroundColor(Color.RED)
            } else if (task.category == "I") {
                tvBadge.text = "IMPORTANT"
                tvBadge.setBackgroundColor(Color.rgb(255, 165, 0)) // Orange
            } else {
                tvBadge.text = "NORMAL"
                tvBadge.setBackgroundColor(Color.BLUE)
            }

            if (task.status == "Done") {
                btnAction.visibility = View.GONE
                tvDuration.visibility = View.VISIBLE
                tvDuration.text = "${task.duration ?: 0} min"
            } else {
                btnAction.visibility = View.VISIBLE
                tvDuration.visibility = View.GONE

                if (task.status == "New") btnAction.text = "TAKE" else btnAction.text = "DONE"

                btnAction.setOnClickListener {
                    val bundle = Bundle()
                    bundle.putInt("ARG_ID", task.id)
                    bundle.putString("ARG_TITLE", task.title)
                    bundle.putString("ARG_DESC", task.description)
                    bundle.putString("ARG_CATEGORY", task.category)
                    bundle.putString("ARG_STATUS", task.status)

                    view.findNavController().navigate(R.id.action_taskDetail_to_actionDetail, bundle)
                }
            }

            return view
        }
    }
}