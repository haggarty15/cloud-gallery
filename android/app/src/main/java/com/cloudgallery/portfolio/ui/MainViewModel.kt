package com.cloudgallery.portfolio.ui

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.google.firebase.auth.FirebaseAuth
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class MainViewModel @Inject constructor() : ViewModel() {

    private val _userEmail = MutableLiveData<String>()
    val userEmail: LiveData<String> = _userEmail

    init {
        val user = FirebaseAuth.getInstance().currentUser
        _userEmail.value = user?.email ?: "Not logged in"
    }
}
