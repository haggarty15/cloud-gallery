package com.cloudgallery.portfolio.data.repository

import android.content.Context
import com.cloudgallery.portfolio.R
import com.cloudgallery.portfolio.data.api.ApiService
import com.cloudgallery.portfolio.data.models.Image
import com.cloudgallery.portfolio.data.models.UploadResponse
import dagger.hilt.android.qualifiers.ApplicationContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository for image operations
 */
@Singleton
class ImageRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val apiService: ApiService
) {
    
    suspend fun uploadImage(
        imageFile: File,
        title: String?,
        description: String?
    ): Result<UploadResponse> {
        return try {
            val requestFile = imageFile.asRequestBody("image/*".toMediaTypeOrNull())
            val filePart = MultipartBody.Part.createFormData("file", imageFile.name, requestFile)
            
            val titlePart = title?.let {
                it.toRequestBody("text/plain".toMediaTypeOrNull())
            }
            
            val descriptionPart = description?.let {
                it.toRequestBody("text/plain".toMediaTypeOrNull())
            }
            
            val response = apiService.uploadImage(filePart, titlePart, descriptionPart)
            
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception(response.message()))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getUserUploads(
        status: String? = null,
        page: Int = 1
    ): Result<List<Image>> {
        return try {
            val response = apiService.getUserUploads(status, page)
            
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!.images)
            } else {
                Result.failure(Exception(response.message()))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteImage(imageId: String): Result<Unit> {
        return try {
            val response = apiService.deleteImage(imageId)
            
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception(response.message()))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
