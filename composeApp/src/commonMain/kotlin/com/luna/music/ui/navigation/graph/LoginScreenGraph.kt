package com.luna.music.ui.navigation.graph

import androidx.compose.foundation.layout.PaddingValues
import androidx.navigation.NavController
import androidx.navigation.NavGraphBuilder
import androidx.navigation.compose.composable
import com.luna.music.ui.navigation.destination.login.DiscordLoginDestination
import com.luna.music.ui.navigation.destination.login.LastfmLoginDestination
import com.luna.music.ui.navigation.destination.login.LoginDestination
import com.luna.music.ui.navigation.destination.login.SpotifyLoginDestination
import com.luna.music.ui.screen.login.DiscordLoginScreen
import com.luna.music.ui.screen.login.DiscordOAuthLoginScreen
import com.luna.music.ui.screen.login.LastfmLoginScreen
import com.luna.music.ui.screen.login.LoginScreen
import com.luna.music.ui.screen.login.SpotifyLoginScreen
import com.luna.discord.isDiscordOAuthAvailable

fun NavGraphBuilder.loginScreenGraph(
    innerPadding: PaddingValues,
    navController: NavController,
    hideBottomBar: () -> Unit,
    showBottomBar: () -> Unit,
) {
    composable<LoginDestination> {
        LoginScreen(
            innerPadding = innerPadding,
            navController = navController,
            hideBottomNavigation = hideBottomBar,
            showBottomNavigation = showBottomBar,
        )
    }

    composable<SpotifyLoginDestination> {
        SpotifyLoginScreen(
            innerPadding = innerPadding,
            navController = navController,
            hideBottomNavigation = hideBottomBar,
            showBottomNavigation = showBottomBar,
        )
    }

    composable<DiscordLoginDestination> {
        // A Full build carries a Discord application and logs in through Discord's own page; a FOSS
        // build keeps the WebView login whose token kizzy uses.
        if (isDiscordOAuthAvailable()) {
            DiscordOAuthLoginScreen(
                innerPadding = innerPadding,
                navController = navController,
                hideBottomNavigation = hideBottomBar,
                showBottomNavigation = showBottomBar,
            )
        } else {
            DiscordLoginScreen(
                innerPadding = innerPadding,
                navController = navController,
                hideBottomNavigation = hideBottomBar,
                showBottomNavigation = showBottomBar,
            )
        }
    }

    composable<LastfmLoginDestination> {
        LastfmLoginScreen(
            innerPadding = innerPadding,
            navController = navController,
            hideBottomNavigation = hideBottomBar,
            showBottomNavigation = showBottomBar,
        )
    }
}