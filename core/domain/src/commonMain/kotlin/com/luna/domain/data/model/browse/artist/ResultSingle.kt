package com.luna.domain.data.model.browse.artist

import com.luna.domain.data.model.searchResult.songs.Thumbnail
import com.luna.domain.data.type.HomeContentType

data class ResultSingle(
    val browseId: String,
    val thumbnails: List<Thumbnail>,
    val title: String,
    val year: String,
) : HomeContentType