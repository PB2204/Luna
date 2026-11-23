package com.luna.music.viewModel

import androidx.lifecycle.viewModelScope
import com.luna.domain.data.entities.NotificationEntity
import com.luna.domain.repository.CommonRepository
import com.luna.music.viewModel.base.BaseViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class NotificationViewModel(
    commonRepository: CommonRepository,
) : BaseViewModel() {
    private var _listNotification: MutableStateFlow<List<NotificationEntity>?> =
        MutableStateFlow(null)
    val listNotification: StateFlow<List<NotificationEntity>?> = _listNotification

    init {
        viewModelScope.launch {
            commonRepository.getAllNotifications().collect { notificationEntities ->
                _listNotification.value =
                    notificationEntities?.sortedByDescending {
                        it.time
                    }
            }
        }
    }
}