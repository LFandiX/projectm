package com.example.activitytest

import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import android.widget.Button
import android.content.Intent
import android.content.Intent.ACTION_DIAL
import android.content.res.Configuration
import android.util.Log


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        Log.d("MainActivity", "TaskID: $taskId")
        setContentView(R.layout.activity_main) // Inflation -> proses membaca dari memori hingga menjadi objek.
        val btn2: Button = findViewById(R.id.mainact)
        btn2.setOnClickListener {
            val intent = Intent(this,MainActivity::class.java)
            startActivity(intent)
        }
        val btn1: Button = findViewById(R.id.button1)

        btn1.setOnClickListener {
            Toast.makeText(this, "Button 1 Clicked!", Toast.LENGTH_LONG).show()
        }

        val destrybtn : Button = findViewById(R.id.button_destroy)

        destrybtn.setOnClickListener {
            finish()
        }

        val openbtn : Button = findViewById( R.id.button_open)

        openbtn.setOnClickListener {
            val intent = Intent(this, SecondActivity::class.java)
            intent.putExtra("extra_data","Alfandi")

            startActivity(intent)
        }


        val implisitintent: Button = findViewById(R.id.button_open2)

        implisitintent.setOnClickListener {
            val intent = Intent("ord.ibda.learn.ACTION_BASIC")
//            startActivity(intent)
//            val intent = Intent(ACTION_DIAl)
            startActivity(intent)
        }

        val commoUI: Button = findViewById(R.id.btnCommonUI)

        commoUI.setOnClickListener {
            val intent = Intent(this, CommonUI::class.java)
            startActivity(intent)
        }




        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
    }

    override fun onStart(){
        super.onStart()
        Log.d("onstart","Onstart")
    }
    override fun onResume(){
        super.onResume()
        Log.d("onresume","Onresume")
    }
    override fun onPause(){
        super.onPause()
        Log.d("onpause","Onpause")
    }
    override fun onStop(){
        super.onStop()
        Log.d("onstop","Onstop")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("ondestroy","Ondestroy")
    }
}