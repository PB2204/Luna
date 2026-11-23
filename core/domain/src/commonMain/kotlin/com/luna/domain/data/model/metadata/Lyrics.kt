package com.luna.domain.data.model.metadata

import kotlinx.serialization.Serializable

@Serializable
data class Lyrics(
    val error: Boolean = false,
    val lines: List<Line>?,
    val syncType: String?,
    val simpMusicLyrics: LunaLyrics? = null,
)

@Serializable
data class LunaLyrics(
    val id: String,
    val vote: Int,
)