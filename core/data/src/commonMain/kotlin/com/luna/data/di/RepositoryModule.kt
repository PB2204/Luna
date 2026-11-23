package com.luna.data.di

import com.luna.common.AppIdentity
import com.luna.common.Config.SERVICE_SCOPE
import com.luna.data.io.fileDir
import com.luna.data.repository.AccountRepositoryImpl
import com.luna.data.repository.AlbumRepositoryImpl
import com.luna.data.repository.AnalyticsRepositoryImpl
import com.luna.data.repository.ArtistRepositoryImpl
import com.luna.data.repository.AutoEqRepositoryImpl
import com.luna.data.lyrics.LyricsRomanizerRepositoryImpl
import com.luna.data.repository.CommonRepositoryImpl
import com.luna.data.repository.DiscordRepositoryImpl
import com.luna.data.repository.HomeRepositoryImpl
import com.luna.data.repository.ImportRepositoryImpl
import com.luna.data.repository.LocalPlaylistRepositoryImpl
import com.luna.data.repository.LyricsCanvasRepositoryImpl
import com.luna.data.repository.PlaylistRepositoryImpl
import com.luna.data.repository.PodcastRepositoryImpl
import com.luna.data.repository.SearchRepositoryImpl
import com.luna.data.repository.SongRepositoryImpl
import com.luna.data.repository.StreamRepositoryImpl
import com.luna.data.repository.TasteRepositoryImpl
import com.luna.data.repository.UpdateRepositoryImpl
import com.luna.domain.repository.AccountRepository
import com.luna.domain.repository.AlbumRepository
import com.luna.domain.repository.AnalyticsRepository
import com.luna.domain.repository.ArtistRepository
import com.luna.domain.repository.AutoEqRepository
import com.luna.domain.repository.LyricsRomanizerRepository
import com.luna.domain.repository.CommonRepository
import com.luna.domain.repository.DiscordRepository
import com.luna.domain.repository.HomeRepository
import com.luna.domain.repository.ImportRepository
import com.luna.domain.repository.LocalPlaylistRepository
import com.luna.domain.repository.LyricsCanvasRepository
import com.luna.domain.repository.PlaylistRepository
import com.luna.domain.repository.PodcastRepository
import com.luna.domain.repository.SearchRepository
import com.luna.domain.repository.SongRepository
import com.luna.domain.repository.StreamRepository
import com.luna.domain.repository.TasteRepository
import com.luna.domain.repository.UpdateRepository
import org.koin.core.qualifier.named
import org.koin.dsl.module

val repositoryModule =
    module {
        single<AccountRepository>(createdAtStart = true) {
            AccountRepositoryImpl(get(), get())
        }

        single<AlbumRepository>(createdAtStart = true) {
            AlbumRepositoryImpl(get(), get())
        }

        single<ArtistRepository>(createdAtStart = true) {
            ArtistRepositoryImpl(get(), get(), get())
        }

        single<CommonRepository>(createdAtStart = true) {
            CommonRepositoryImpl(get(named(SERVICE_SCOPE)), get(), get(), get(), get(), get()).apply {
                this.init("${fileDir()}/ytdlp-cookie.txt", get(), get<AppIdentity>().isDevBuild)
            }
        }

        // At start: a Full build drops the token kizzy's login left behind as soon as it launches.
        single<DiscordRepository>(createdAtStart = true) {
            DiscordRepositoryImpl(get())
        }

        // Lazy for the same reason its client is: the picker is the only thing that wants it.
        single<AutoEqRepository> {
            AutoEqRepositoryImpl(get(), get())
        }

        // Lazy: constructing it costs a few File.length() calls (plus, while the pack is missing,
        // one background read of the stored selection), but the kuromoji dictionary behind it is
        // loaded on first Japanese line, or right after a download installs it, and never at
        // startup — so this must NOT be createdAtStart, or every launch pays for a feature most
        // listeners leave off. The path is where Android keeps the downloaded ipadic pack (the
        // APK no longer bundles it); Desktop and iOS ignore it.
        single<LyricsRomanizerRepository> {
            LyricsRomanizerRepositoryImpl("${fileDir()}/kuromoji-ipadic", get())
        }

        single<HomeRepository>(createdAtStart = true) {
            HomeRepositoryImpl(get(), get())
        }

        single<ImportRepository>(createdAtStart = true) {
            ImportRepositoryImpl(get())
        }

        single<LocalPlaylistRepository>(createdAtStart = true) {
            LocalPlaylistRepositoryImpl(get(), get())
        }

        single<LyricsCanvasRepository>(createdAtStart = true) {
            LyricsCanvasRepositoryImpl(get(), get(), get(), get(), get())
        }

        single<PlaylistRepository>(createdAtStart = true) {
            PlaylistRepositoryImpl(get(), get(), get())
        }

        single<PodcastRepository>(createdAtStart = true) {
            PodcastRepositoryImpl(get(), get())
        }

        single<SearchRepository>(createdAtStart = true) {
            SearchRepositoryImpl(get(), get())
        }

        single<SongRepository>(createdAtStart = true) {
            SongRepositoryImpl(get(), get(), get())
        }

        single<StreamRepository>(createdAtStart = true) {
            StreamRepositoryImpl(get(), get())
        }

        single<UpdateRepository>(createdAtStart = true) {
            UpdateRepositoryImpl(get())
        }

        single<AnalyticsRepository>(createdAtStart = true) {
            AnalyticsRepositoryImpl(get())
        }

        // Lazy: only the taste card in Library asks for it.
        single<TasteRepository> {
            TasteRepositoryImpl(get(), get())
        }
    }