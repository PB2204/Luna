package com.luna.music.di

import com.luna.music.viewModel.AlbumViewModel
import com.luna.music.utils.VersionManager
import com.luna.music.viewModel.AnalyticsViewModel
import com.luna.music.viewModel.ListenTogetherSettingsViewModel
import com.luna.music.viewModel.ListenTogetherViewModel
import com.luna.music.viewModel.ArtistViewModel
import com.luna.music.viewModel.BrowseViewModel
import com.luna.music.viewModel.BrowserLoginViewModel
import com.luna.music.viewModel.CommentsViewModel
import com.luna.music.viewModel.RadioBuilderViewModel
import com.luna.music.viewModel.SoundCloudPlayerViewModel
import com.luna.music.viewModel.HomeViewModel
import com.luna.music.viewModel.ImportViewModel
import com.luna.music.viewModel.LibraryDynamicPlaylistViewModel
import com.luna.music.viewModel.LibrarySidebarViewModel
import com.luna.music.viewModel.LibraryViewModel
import com.luna.music.viewModel.LocalPlaylistViewModel
import com.luna.music.viewModel.LibrarySyncHostViewModel
import com.luna.music.viewModel.LibrarySyncPhoneViewModel
import com.luna.music.viewModel.LogInViewModel
import com.luna.music.viewModel.LoginSyncHostViewModel
import com.luna.music.viewModel.LoginSyncSenderViewModel
import com.luna.music.viewModel.MoodViewModel
import com.luna.music.viewModel.MoreAlbumsViewModel
import com.luna.music.viewModel.NotificationViewModel
import com.luna.music.viewModel.NowPlayingBottomSheetViewModel
import com.luna.music.viewModel.PlaylistViewModel
import com.luna.music.viewModel.PodcastViewModel
import com.luna.music.viewModel.SearchViewModel
import com.luna.music.viewModel.AutoEqViewModel
import com.luna.music.viewModel.SettingsViewModel
import com.luna.music.viewModel.SharedViewModel
import com.luna.music.viewModel.SongSelectionViewModel
import com.luna.music.viewModel.TasteViewModel
import com.luna.music.viewModel.WrappedViewModel
import org.koin.core.module.dsl.viewModel
import org.koin.dsl.module

val viewModelModule =
    module {
        single {
            SharedViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        single {
            SearchViewModel(
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            SongSelectionViewModel(
                get(),
                get(),
            )
        }
        // Only one of these resolves on a given platform: Desktop binds the host repository, Android the
        // sender. Koin resolves dependencies when a ViewModel is created, not when it is declared.
        viewModel { LoginSyncHostViewModel(get()) }
        viewModel { LoginSyncSenderViewModel(get(), get()) }
        viewModel { LibrarySyncHostViewModel(get()) }
        viewModel { LibrarySyncPhoneViewModel(get()) }
        viewModel { BrowserLoginViewModel(get()) }
        viewModel { CommentsViewModel(get(), get()) }
        viewModel { SoundCloudPlayerViewModel(get()) }
        viewModel {
            NowPlayingBottomSheetViewModel(
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            LibraryViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            LibraryDynamicPlaylistViewModel(
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            ImportViewModel(
                get(),
            )
        }
        viewModel {
            AlbumViewModel(
                get(),
                get(),
            )
        }
        viewModel {
            HomeViewModel(
                get(),
                get(),
            )
        }
        viewModel {
            AutoEqViewModel(
                get(),
                get(),
            )
        }
        viewModel {
            SettingsViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            ArtistViewModel(
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            PlaylistViewModel(
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            LogInViewModel(
                get(),
                get(),
            )
        }
        viewModel {
            PodcastViewModel(
                get(),
            )
        }
        viewModel {
            MoreAlbumsViewModel(
                get(),
            )
        }
        viewModel {
            BrowseViewModel(
                get(),
            )
        }
        viewModel {
            RadioBuilderViewModel(
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            LibrarySidebarViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            LocalPlaylistViewModel(
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            NotificationViewModel(
                get(),
            )
        }
        viewModel {
            MoodViewModel(
                get(),
                get(),
            )
        }
        viewModel {
            AnalyticsViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            WrappedViewModel(
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            TasteViewModel(
                get(),
                get(),
                get(),
                get(),
                get(),
                get(),
            )
        }
        viewModel {
            ListenTogetherSettingsViewModel(get())
        }
        viewModel {
            ListenTogetherViewModel(
                repository = get(),
                dataStore = get(),
                bridge = get(),
            )
        }

    }
