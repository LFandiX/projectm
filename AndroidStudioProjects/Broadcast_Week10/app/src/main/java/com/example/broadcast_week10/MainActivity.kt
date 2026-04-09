package com.example.broadcast_week10

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.content.Intent
import android.content.IntentFilter
import android.widget.Button

class MainActivity : AppCompatActivity() {
    lateinit var timeChangeReceiver: TimeChangeReceiver


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        timeChangeReceiver = TimeChangeReceiver()

        // Dynamic Registration
        val intentFilter = IntentFilter()
        intentFilter.addAction("android.intent.action.TIME_TICK")
        registerReceiver(timeChangeReceiver,intentFilter)

        val mybtn = findViewById<Button>(R.id.my_button)
        mybtn.setOnClickListener {
            val intent = Intent("com.example.broadcast_week10.MY_BROADCAST")
            intent.setPackage(packageName)
            // sendBroadcast(intent)
            sendOrderedBroadcast(intent, null)



        }


        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(timeChangeReceiver)
    }


}