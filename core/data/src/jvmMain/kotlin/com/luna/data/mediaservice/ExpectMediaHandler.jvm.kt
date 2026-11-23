package com.luna.data.mediaservice

import com.luna.domain.repository.AnalyticsRepository
import com.luna.domain.repository.DiscordRepository

actual fun createMediaServiceHandler(
    dataStoreManager: com.luna.domain.manager.DataStoreManager,
    songRepository: com.luna.domain.repository.SongRepository,
    streamRepository: com.luna.domain.repository.StreamRepository,
    localPlaylistRepository: com.luna.domain.repository.LocalPlaylistRepository,
    analyticsRepository: AnalyticsRepository,
    discordRepository: DiscordRepository,
    coroutineScope: kotlinx.coroutines.CoroutineScope,
): com.luna.domain.mediaservice.handler.MediaPlayerHandler =
    JvmMediaPlayerHandlerImpl(
        dataStoreManager = dataStoreManager,
        songRepository = songRepository,
        streamRepository = streamRepository,
        localPlaylistRepository = localPlaylistRepository,
        analyticsRepository = analyticsRepository,
        discordRepository = discordRepository,
        coroutineScope = coroutineScope,
    )