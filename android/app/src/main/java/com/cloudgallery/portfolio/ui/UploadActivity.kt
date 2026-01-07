package com.cloudgallery.portfolio.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.cloudgallery.portfolio.databinding.ActivityUploadBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class UploadActivity : AppCompatActivity() {
    private lateinit var binding: ActivityUploadBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUploadBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupToolbar()
    }

    private fun setupToolbar() {
        setSupportActionBar(null) // Or use a proper toolbar if added to layout
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        title = "Upload Photo"
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}
