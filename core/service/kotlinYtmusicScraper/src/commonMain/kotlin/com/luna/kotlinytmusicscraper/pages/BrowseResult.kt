package com.luna.kotlinytmusicscraper.pages

import com.luna.kotlinytmusicscraper.models.YTItem

data class BrowseResult(
    val title: String?,
    val items: List<Item>,
) {
    data class Item(
        val title: String?,
        val items: List<YTItem>,
        /** Mood & genre buttons: not [YTItem]s, so they ride alongside. */
        val moods: List<MoodAndGenres.Item> = emptyList(),
    )
}