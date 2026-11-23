package com.luna.data.di.loader

import com.luna.media_jvm.di.loadDesktopPlayerModule
import com.luna.data.browserlogin.BrowserLoginRepositoryImpl
import com.luna.data.librarysync.LibrarySyncHostRepositoryImpl
import com.luna.data.librarysync.SyncApplier
import com.luna.data.librarysync.SyncEngine
import com.luna.data.librarysync.SyncedSettings
import com.luna.data.loginsync.LoginSyncHostRepositoryImpl
import com.luna.data.loginsync.LoginSyncStore
import com.luna.domain.repository.LibrarySyncHostRepository
import com.luna.domain.repository.LibrarySyncRepository
import com.luna.domain.repository.LoginSyncHostRepository
import com.luna.domain.repository.BrowserLoginRepository
import org.koin.core.context.loadKoinModules
import org.koin.dsl.module

actual fun loadMediaService() {
    loadDesktopPlayerModule()
}

actual fun loadLoginSyncModule() {
    loadKoinModules(
        module {
            single { LoginSyncStore(get(), get(), get()) }
            single<LoginSyncHostRepository> { LoginSyncHostRepositoryImpl(get()) }
            // Library sync (#2663): this computer keeps the log and serves its paired phones.
            single { SyncedSettings(get(), get()) }
            single { SyncEngine(get(), get(), SyncApplier(get(), get()), get()) }
            single<LibrarySyncHostRepository> { LibrarySyncHostRepositoryImpl(get(), get(), get(), get(), get(), get()) }
            single<LibrarySyncRepository> { get<LibrarySyncHostRepository>() }
            single<BrowserLoginRepository> { BrowserLoginRepositoryImpl() }
        },
    )
}
