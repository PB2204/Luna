package com.luna.data.db

import androidx.room.Room
import androidx.room.RoomDatabase
import com.luna.common.DB_NAME
import com.luna.data.io.getHomeFolderPath
import java.io.File

actual fun getDatabaseBuilder(
    converters: Converters
): RoomDatabase.Builder<MusicDatabase> {
    return Room.databaseBuilder<MusicDatabase>(
        name = getDatabasePath()
    ).addTypeConverter(converters)
}

actual fun getDatabasePath(): String {
    val dbFile = File(getHomeFolderPath(listOf(".luna", "db")), DB_NAME)
    return dbFile.absolutePath
}