package com.luna.kotlinytmusicscraper.pages

import com.luna.kotlinytmusicscraper.models.SongItem

data class PlaylistContinuationPage(
    val songs: List<SongItem>,
    val continuation: String?,
)