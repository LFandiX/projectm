package com.example.framing_week9

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
//// TODO: Rename parameter arguments, choose names that match
//// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
//private const val ARG_PARAM1 = "param1"
//private const val ARG_PARAM2 = "param2"

/**4
 * A simple [Fragment] subclass.
 * Use the [LeftFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class LeftFragment : Fragment() {


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment

        val _root = inflater.inflate(R.layout.fragment_left, container, false)
        val fragmentABtn = _root.findViewById<Button>(R.id.fragmentA)
        fragmentABtn.setOnClickListener {

            if (activity != null){
                val mainActivity = activity as MainActivity

                mainActivity.test()
                mainActivity.replaceFragment(AFragment())


            }



        }


        val fragmentBBtn = _root.findViewById<Button>(R.id.fragmentB)
        fragmentBBtn.setOnClickListener {

            if (activity != null){
                val mainActivity = activity as MainActivity

                mainActivity.test()
                mainActivity.replaceFragment(BFragment())


            }



        }


        return _root
    }

}