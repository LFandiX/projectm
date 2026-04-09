package com.example.broadcast_week10


import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.widget.Toast

class TimeChangeReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context?, intent: Intent?) {
        Toast.makeText(context, "Time has change!!", Toast.LENGTH_LONG).show()
    }

}