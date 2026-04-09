package com.example.bibleverse.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.bibleverse.R
import com.example.bibleverse.databinding.ItemReadingBinding
import com.example.bibleverse.model.ReadingChapter

class ReadingAdapter(
    private val chapters: List<ReadingChapter>,
    private val journaledChapters: Set<String>,
    private val onClick: (ReadingChapter) -> Unit
) : RecyclerView.Adapter<ReadingAdapter.ViewHolder>() {

    class ViewHolder(val binding: ItemReadingBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemReadingBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val chapter = chapters[position]
        holder.binding.chapterText.text = "${chapter.book} ${chapter.chapter}"
        
        val key = "${chapter.book}_${chapter.chapter}"
        if (journaledChapters.contains(key)) {
            holder.binding.statusIcon.setImageResource(R.drawable.ic_check_circle)
            holder.binding.statusIcon.setColorFilter(holder.itemView.context.getColor(R.color.green_700))
        } else {
            holder.binding.statusIcon.setImageResource(R.drawable.ic_chevron_right)
            holder.binding.statusIcon.setColorFilter(holder.itemView.context.getColor(R.color.stone_400))
        }
        
        holder.itemView.setOnClickListener { onClick(chapter) }
    }

    override fun getItemCount() = chapters.size
}
