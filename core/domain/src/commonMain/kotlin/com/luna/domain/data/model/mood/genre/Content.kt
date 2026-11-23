package com.luna.domain.data.model.mood.genre

import com.luna.domain.data.model.searchResult.songs.Thumbnail
import com.luna.domain.data.type.HomeContentType

data class Content(
    val playlistBrowseId: String,
    val thumbnail: List<Thumbnail>?,
    val title: Title,
) : HomeContentType