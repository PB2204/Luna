package com.luna.data.mediaservice

import com.luna.domain.manager.DataStoreManager
import com.luna.domain.mediaservice.handler.MediaPlayerHandler
import com.luna.domain.repository.AnalyticsRepository
import com.luna.domain.repository.DiscordRepository
import com.luna.domain.repository.LocalPlaylistRepository
import com.luna.domain.repository.SongRepository
import com.luna.domain.repository.StreamRepository
import kotlinx.coroutines.CoroutineScope

expect fun createMediaServiceHandler(
    dataStoreManager: DataStoreManager,
    songRepository: SongRepository,
    streamRepository: StreamRepository,
    localPlaylistRepository: LocalPlaylistRepository,
    analyticsRepository: AnalyticsRepository,
    discordRepository: DiscordRepository,
    coroutineScope: CoroutineScope,
): MediaPlayerHandler