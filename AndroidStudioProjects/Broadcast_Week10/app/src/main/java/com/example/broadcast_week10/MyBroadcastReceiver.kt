package com.example.broadcast_week10

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.widget.Toast

class MyBroadcastReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        Toast.makeText(context, "Receive in my Phone!!", Toast.LENGTH_LONG).show()
        abortBroadcast() // untuk keep sendiri
    }
}