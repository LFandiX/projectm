package com.example.taskinventoryapp

import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.ImageButton
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import com.example.taskinventory.api.RetrofitClient
import com.example.taskinventory.model.Task
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController

class TaskDetail : Fragment() {

    // --- BAGIAN 1: VARIABEL UI ---
    private lateinit var lvTaskList: ListView
    private lateinit var tvPageTitle: TextView
    private lateinit var btnFilterN: Button
    private lateinit var btnFilterU: Button
    private lateinit var btnFilterI: Button

    // Adapter kita panggil disini
    private lateinit var adapter: SimpleTaskAdapter
    private var allTasks: List<Task> = listOf()

    // Variabel Filter
    private var currentStatusFilter = "New"
    private var currentCategoryFilter = "All"

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Hubungkan ke layout XML kamu (pastikan namanya benar, misal fragment_task_list)
        return inflater.inflate(R.layout.fragment_task_detail, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // --- BAGIAN 2: INIT VIEW ---
        lvTaskList = view.findViewById(R.id.lvTaskList)
        tvPageTitle = view.findViewById(R.id.tvPageTitle)
        btnFilterN = view.findViewById(R.id.btnFilterN)
        btnFilterU = view.findViewById(R.id.btnFilterU)
        btnFilterI = view.findViewById(R.id.btnFilterI)
        val backBtn = view.findViewById<ImageButton>(R.id.btnBack)
        backBtn.setOnClickListener {
            findNavController().popBackStack()
        }
        // Ambil data kiriman dari Home
        arguments?.let {
            currentStatusFilter = it.getString("STATUS_FILTER", "New")
        }
        tvPageTitle.text = "$currentStatusFilter Tasks"

        // --- BAGIAN 3: PASANG ADAPTER (Disini kuncinya) ---
        // Kita pakai adapter yang kita tulis di bawah (Inner Class)
        adapter = SimpleTaskAdapter(requireContext())
        lvTaskList.adapter = adapter

        // Panggil API
        loadDataDariServer()

        // Setup Filter
        btnFilterN.setOnClickListener { currentCategoryFilter = "N"; saringData() }
        btnFilterU.setOnClickListener { currentCategoryFilter = "U"; saringData() }
        btnFilterI.setOnClickListener { currentCategoryFilter = "I"; saringData() }
    }

    private fun loadDataDariServer() {
        val call = RetrofitClient.instance.getAllTasks()
        call.enqueue(object : Callback<List<Task>> {
            override fun onResponse(call: Call<List<Task>>, response: Response<List<Task>>) {
                if (response.isSuccessful) {
                    allTasks = response.body() ?: emptyList()
                    saringData() // Tampilkan data setelah loading selesai
                }
            }
            override fun onFailure(call: Call<List<Task>>, t: Throwable) {
                if(context != null) Toast.makeText(context, "Error Koneksi", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun saringData() {
        // Logic penyaring data (Filter)
        val hasilSaringan = allTasks.filter { task ->
            val statusCocok = task.status == currentStatusFilter && task.deleted == "False"
            val kategoriCocok = if (currentCategoryFilter == "All") true else task.category == currentCategoryFilter
            statusCocok && kategoriCocok
        }

        // Masukkan data hasil saringan ke Adapter agar muncul di layar
        adapter.isiData(hasilSaringan)
    }

    // =========================================================================
    // BAGIAN INI ADALAH ADAPTERNYA (INNER CLASS)
    // Tulis saja di dalam file ini (di paling bawah), jadi tidak perlu file baru
    // =========================================================================
    inner class SimpleTaskAdapter(private val context: Context) : BaseAdapter() {

        var listData: List<Task> = ArrayList()

        // Fungsi untuk update data dari Fragment
        fun isiData(dataBaru: List<Task>) {
            listData = dataBaru
            notifyDataSetChanged() // Refresh layar otomatis
        }

        // 3 Fungsi Wajib ListView (Hapal mati saja, isinya standar)
        override fun getCount(): Int = listData.size
        override fun getItem(position: Int): Any = listData[position]
        override fun getItemId(position: Int): Long = position.toLong()

        // Fungsi Inti: Menggambar Tampilan Per Baris
        override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
            var view = convertView
            if (view == null) {
                // Tempelkan layout kotak (item_task.xml)
                view = LayoutInflater.from(context).inflate(R.layout.item_task, parent, false)
            }

            // Ambil data task nomor sekian
            val task = listData[position]

            // Hubungkan ID yang ada di item_task.xml
            val tvTitle = view!!.findViewById<TextView>(R.id.tvTaskTitle)
            val tvTime = view.findViewById<TextView>(R.id.tvTaskTime)
            val tvBadge = view.findViewById<TextView>(R.id.tvCategoryBadge)
            val btnAction = view.findViewById<Button>(R.id.btnAction)
            val tvDuration = view.findViewById<TextView>(R.id.tvDuration)

            // Isi Datanya
            tvTitle.text = task.title
            tvTime.text = task.createdTime

            // Warna Badge Kategori
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

            // Atur Tombol
            if (task.status == "Done") {
                btnAction.visibility = View.GONE
                tvDuration.visibility = View.VISIBLE
                tvDuration.text = "${task.duration ?: 0} min"
            } else {
                btnAction.visibility = View.VISIBLE
                tvDuration.visibility = View.GONE

                if (task.status == "New") btnAction.text = "TAKE" else btnAction.text = "DONE"

                // KLIK TOMBOL -> PINDAH KE SCENE 3
                btnAction.setOnClickListener {
                    val bundle = Bundle()
                    bundle.putInt("ARG_ID", task.id)
                    bundle.putString("ARG_TITLE", task.title)
                    bundle.putString("ARG_DESC", task.description)
                    bundle.putString("ARG_CATEGORY", task.category)
                    bundle.putString("ARG_STATUS", task.status)

                    // Pindah Layar
                    view.findNavController().navigate(R.id.action_taskDetail_to_actionDetail, bundle)
                }
            }

            return view
        }
    }
}