package com.cloudgallery.portfolio

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * Application class for dependency injection initialization
 */
@HiltAndroidApp
class GalleryApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        // Initialize any required libraries here
    }
}
