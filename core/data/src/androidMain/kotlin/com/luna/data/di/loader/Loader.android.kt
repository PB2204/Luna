package com.luna.data.di.loader

import com.luna.media3.di.loadMediaService
import com.luna.data.librarysync.LibrarySyncPhoneRepositoryImpl
import com.luna.data.librarysync.SyncApplier
import com.luna.data.librarysync.SyncEngine
import com.luna.data.librarysync.SyncedSettings
import com.luna.data.loginsync.LoginSyncSenderRepositoryImpl
import com.luna.data.loginsync.LoginSyncStore
import com.luna.domain.repository.LibrarySyncPhoneRepository
import com.luna.domain.repository.LibrarySyncRepository
import com.luna.domain.repository.LoginSyncSenderRepository
import org.koin.core.context.loadKoinModules
import com.luna.loginsync.LoginSyncClient
import com.luna.loginsync.PairedSyncClient
import org.koin.dsl.module

actual fun loadMediaService() {
    loadMediaService()
}

actual fun loadLoginSyncModule() {
    loadKoinModules(
        module {
            single { LoginSyncStore(get(), get(), get()) }
            single<LoginSyncSenderRepository> { LoginSyncSenderRepositoryImpl(get(), LoginSyncClient()) }
            // Library sync (#2663): this phone drives every round with the computer it is paired with.
            single { SyncedSettings(get(), get()) }
            single { SyncEngine(get(), get(), SyncApplier(get(), get()), get()) }
            single<LibrarySyncPhoneRepository> {
                LibrarySyncPhoneRepositoryImpl(get(), get(), get(), get(), get(), get(), get(), PairedSyncClient())
            }
            single<LibrarySyncRepository> { get<LibrarySyncPhoneRepository>() }
        },
    )
}
