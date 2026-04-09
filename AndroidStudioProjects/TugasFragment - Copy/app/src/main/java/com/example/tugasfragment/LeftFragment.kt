package com.example.tugasfragment

import android.content.Intent
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ListView
import android.widget.Toast

class LeftFragment : Fragment() {



    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val _root = inflater.inflate(R.layout.fragment_left, container, false)

        // 1. Siapkan data untuk ditampilkan di ListView
        val fragmentOptions = arrayOf("Display Fragment A", "Display Fragment B", "Display Fragment C")

        // 2. Temukan komponen ListView dari layout
        val listView = _root.findViewById<ListView>(R.id.fragment_list_view)

        // 3. Buat Adapter untuk menghubungkan data dengan ListView
        // Kita gunakan layout bawaan Android yang simpel untuk setiap item
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_list_item_1, fragmentOptions)

        // 4. Set adapter ke ListView
        listView.adapter = adapter

        // 5. Atur listener untuk menangani klik pada setiap item di ListView
        listView.setOnItemClickListener { parent, view, position, id ->
            if (activity != null) {
                val mainActivity = activity as MainActivity

                mainActivity.test()

                when (position) {
                    0 -> {
                        mainActivity.replaceFragment(AFragment())
                    }
                    1 -> {
                        mainActivity.replaceFragment(BFragment())
                    }
                    2 -> {
                        mainActivity.replaceFragment(CFragment())
                    }
                }
            }
        }









        return _root
    }


}