package com.example.constrainlayout

import android.app.Activity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.TextView
import org.w3c.dom.Text

class FruitAdapter(activity: Activity, val restId:Int, data: List<Fruit>): ArrayAdapter<Fruit>(
    activity,restId,data) {
    inner class ViewHolder(val fruitImafe: ImageView,val fruitName: TextView)

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
//        return super.getView(position, convertView, parent)
        val _view: View
        val viewHolder: ViewHolder
        if (convertView == null){
            _view = LayoutInflater.from(context).inflate(restId,parent,false)
            val fruitImage = _view.findViewById<ImageView>(R.id.fruitImage)
            val fruitName = _view.findViewById<TextView>(R.id.fruitName)
            viewHolder = ViewHolder(fruitImage,fruitName)

            _view.tag = viewHolder

        } else{
            _view = convertView
            viewHolder = _view.tag as ViewHolder
        }
//        val _view = LayoutInflater.from(context).inflate(restId,parent,false)

        val fruitImage = _view.findViewById<ImageView>(R.id.fruitImage)
        val fruitName = _view.findViewById<TextView>(R.id.fruitName)
        val fruit = getItem(position)

        if (fruit != null){
            fruitName.text = fruit.name
            fruitImage.setImageResource(fruit.imageId)
        }

        return _view
    }





}