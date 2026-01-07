package com.cloudgallery.portfolio.ui.coloring

import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.cloudgallery.portfolio.R
import com.cloudgallery.portfolio.databinding.ItemColorPickerBinding
import com.cloudgallery.portfolio.data.models.ColorInfo

/**
 * Color Picker Adapter - Horizontal scrollable color palette
 */
class ColorPickerAdapter(
    private val onColorSelected: (ColorInfo) -> Unit
) : ListAdapter<ColorInfo, ColorPickerAdapter.ColorViewHolder>(ColorDiffCallback()) {

    private var selectedColorNum: Int = 1

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ColorViewHolder {
        val binding = ItemColorPickerBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ColorViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ColorViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    fun setSelectedColor(colorNum: Int) {
        val previousSelected = selectedColorNum
        selectedColorNum = colorNum
        
        // Update only affected items
        currentList.forEachIndexed { index, color ->
            if (color.num == previousSelected || color.num == selectedColorNum) {
                notifyItemChanged(index)
            }
        }
    }

    inner class ColorViewHolder(
        private val binding: ItemColorPickerBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(colorInfo: ColorInfo) {
            // Set color number
            binding.tvColorNumber.text = colorInfo.num.toString()

            // Set color circle
            val color = colorInfo.toAndroidColor()
            val drawable = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(color)
                setStroke(
                    if (colorInfo.num == selectedColorNum) 8 else 2,
                    if (colorInfo.num == selectedColorNum) {
                        ContextCompat.getColor(binding.root.context, R.color.color_picker_selected)
                    } else {
                        Color.GRAY
                    }
                )
            }
            binding.colorCircle.background = drawable

            // Set hex text
            binding.tvColorHex.text = colorInfo.hex

            // Click listener
            binding.root.setOnClickListener {
                onColorSelected(colorInfo)
            }

            // Scale animation for selected color
            val scale = if (colorInfo.num == selectedColorNum) 1.2f else 1.0f
            binding.colorCircle.scaleX = scale
            binding.colorCircle.scaleY = scale
        }
    }

    private class ColorDiffCallback : DiffUtil.ItemCallback<ColorInfo>() {
        override fun areItemsTheSame(oldItem: ColorInfo, newItem: ColorInfo): Boolean {
            return oldItem.num == newItem.num
        }

        override fun areContentsTheSame(oldItem: ColorInfo, newItem: ColorInfo): Boolean {
            return oldItem == newItem
        }
    }
}
