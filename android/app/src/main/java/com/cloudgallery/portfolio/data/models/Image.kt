package com.cloudgallery.portfolio.data.models

import com.google.gson.annotations.SerializedName

/**
 * Image data model
 */
data class Image(
    val id: String,
    @SerializedName("user_id")
    val userId: String,
    @SerializedName("user_name")
    val userName: String?,
    val title: String?,
    val description: String?,
    val status: String, // pending, approved, rejected
    @SerializedName("image_url")
    val imageUrl: String?,
    @SerializedName("thumbnail_url")
    val thumbnailUrl: String?,
    @SerializedName("uploaded_at")
    val uploadedAt: String?,
    @SerializedName("reviewed_at")
    val reviewedAt: String?,
    @SerializedName("reviewed_by")
    val reviewedBy: String?,
    val metadata: ImageMetadata?
)

data class ImageMetadata(
    @SerializedName("mime_type")
    val mimeType: String?,
    @SerializedName("file_size")
    val fileSize: Long?,
    val width: Int?,
    val height: Int?
)

data class UploadResponse(
    val success: Boolean,
    @SerializedName("image_id")
    val imageId: String?,
    val status: String?,
    val message: String?
)

data class ImageListResponse(
    val images: List<Image>,
    val pagination: Pagination
)

data class Pagination(
    val page: Int,
    val limit: Int,
    val total: Int,
    val pages: Int
)

data class ErrorResponse(
    val error: String,
    val code: String?,
    val details: Map<String, Any>?
)
