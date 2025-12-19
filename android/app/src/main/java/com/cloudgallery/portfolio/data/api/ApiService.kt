package com.cloudgallery.portfolio.data.api

import com.cloudgallery.portfolio.data.models.ImageListResponse
import com.cloudgallery.portfolio.data.models.UploadResponse
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit API service interface
 */
interface ApiService {
    
    @Multipart
    @POST("api/upload")
    suspend fun uploadImage(
        @Part file: MultipartBody.Part,
        @Part("title") title: RequestBody?,
        @Part("description") description: RequestBody?
    ): Response<UploadResponse>
    
    @GET("api/uploads")
    suspend fun getUserUploads(
        @Query("status") status: String?,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): Response<ImageListResponse>
    
    @DELETE("api/images/{imageId}")
    suspend fun deleteImage(
        @Path("imageId") imageId: String
    ): Response<Map<String, Any>>
    
    @GET("api/gallery")
    suspend fun getGallery(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20,
        @Query("sort") sort: String = "newest"
    ): Response<ImageListResponse>
}
