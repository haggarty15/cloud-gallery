package com.cloudgallery.portfolio.ui

import android.content.Intent
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import com.cloudgallery.portfolio.databinding.ActivityMainBinding
import com.cloudgallery.portfolio.ui.gallery.GalleryActivity
import com.google.firebase.auth.FirebaseAuth
import dagger.hilt.android.AndroidEntryPoint

/**
 * Main Activity - Entry point of the app
 */
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()
    private val auth = FirebaseAuth.getInstance()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        checkAuthState()
        setupUI()
        observeViewModel()
    }
    
    private fun checkAuthState() {
        if (auth.currentUser == null) {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
    
    private fun setupUI() {
        binding.cardUpload.setOnClickListener {
            startActivity(Intent(this, UploadActivity::class.java))
        }
        
        binding.cardGallery.setOnClickListener {
            startActivity(Intent(this, GalleryActivity::class.java))
        }
        
        binding.btnLogout.setOnClickListener {
            auth.signOut()
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }
    
    private fun observeViewModel() {
        viewModel.userEmail.observe(this) { email ->
            binding.tvUserEmail.text = email
        }
    }
}
