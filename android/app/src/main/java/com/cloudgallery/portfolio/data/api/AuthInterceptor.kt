package com.cloudgallery.portfolio.data.api

import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.tasks.await
import okhttp3.Interceptor
import okhttp3.Response

/**
 * Interceptor to add Firebase auth token to requests
 */
class AuthInterceptor : Interceptor {
    
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        
        // Get Firebase auth token
        val token = runBlocking {
            try {
                FirebaseAuth.getInstance().currentUser?.getIdToken(false)?.await()?.token
            } catch (e: Exception) {
                null
            }
        }
        
        // Add auth header if token exists
        val request = if (token != null) {
            original.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            original
        }
        
        return chain.proceed(request)
    }
}
