package com.cloudgallery.portfolio.ui.gallery

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import coil.load
import com.cloudgallery.portfolio.R
import com.cloudgallery.portfolio.databinding.ItemCompletedColoringBinding
import com.cloudgallery.portfolio.data.models.ColoringSession

class CompletedColoringsAdapter(
    private val onColoringClick: (ColoringSession) -> Unit
) : ListAdapter<ColoringSession, CompletedColoringsAdapter.ViewHolder>(SessionDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemCompletedColoringBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ViewHolder(
        private val binding: ItemCompletedColoringBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(session: ColoringSession) {
            binding.apply {
                tvProgress.text = "${session.completionPercent}% Complete"
                
                // Load colored result image
                ivColoring.load(session.coloredImageUrl) {
                    crossfade(true)
                    placeholder(R.drawable.placeholder_image)
                    error(R.drawable.error_image)
                }

                root.setOnClickListener {
                    onColoringClick(session)
                }
            }
        }
    }

    private class SessionDiffCallback : DiffUtil.ItemCallback<ColoringSession>() {
        override fun areItemsTheSame(oldItem: ColoringSession, newItem: ColoringSession) =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: ColoringSession, newItem: ColoringSession) =
            oldItem == newItem
    }
}
