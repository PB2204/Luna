package com.luna.music.ui.component

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.LinkAnnotation
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextLinkStyles
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withLink
import androidx.compose.ui.window.DialogProperties
import com.luna.music.expect.openUrl
import com.luna.music.ui.theme.seed
import com.luna.music.ui.theme.typo
import org.jetbrains.compose.resources.painterResource
import org.jetbrains.compose.resources.stringResource
import luna.composeapp.generated.resources.*

@Composable
@ExperimentalMaterial3Api
fun ReviewDialog(
    onDismissRequest: () -> Unit,
    onDoneReview: () -> Unit,
) {
    val uriHandler = LocalUriHandler.current
    AlertDialog(
        properties =
            DialogProperties(
                dismissOnBackPress = false,
                dismissOnClickOutside = false,
            ),
        onDismissRequest = {
            onDismissRequest.invoke()
        },
        confirmButton = {
            TextButton(onClick = {
                onDoneReview.invoke()
                uriHandler.openUri("https://github.com/PB2204/Luna")
            }) {
                Text(
                    stringResource(Res.string.give_a_star),
                    style = typo().bodySmall,
                )
            }
        },
        dismissButton = {
            TextButton(onClick = {
                onDismissRequest.invoke()
            }) {
                Text(
                    stringResource(Res.string.later),
                    style = typo().bodySmall,
                )
            }
        },
        icon = {
            Icon(painterResource(Res.drawable.mono), "App Icon")
        },
        title = {
            Text(
                stringResource(Res.string.enjoying_luna),
                style = typo().labelSmall,
            )
        },
        text = {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    buildAnnotatedString {
                        append(stringResource(Res.string.if_you_enjoy_using_luna_star_luna_on_github_or_leave_a_review_on))
                        withLink(
                            LinkAnnotation.Url(
                                "https://www.producthunt.com/products/luna",
                                TextLinkStyles(style = SpanStyle(textDecoration = TextDecoration.Underline, color = seed)),
                            ) {
                                onDoneReview.invoke()
                                onDismissRequest.invoke()
                                uriHandler.openUri("https://www.producthunt.com/products/luna")
                            },
                        ) {
                            append(" ProductHunt")
                        }
                        append("\n")
                        // Every locale wraps this in quotes to keep the trailing space, Android style, and Compose
                        // Resources prints them as text. Strip them and add the space here, like " ProductHunt" above.
                        append(stringResource(Res.string.if_you_love_my_work_consider).removeSurrounding("\"").trimEnd() + " ")
                        withLink(
                            LinkAnnotation.Url(
                                "https://github.com/sponsors/PB2204",
                                TextLinkStyles(style = SpanStyle(textDecoration = TextDecoration.Underline, color = seed)),
                            ) {
                                onDoneReview.invoke()
                                onDismissRequest.invoke()
                                uriHandler.openUri("https://github.com/sponsors/PB2204")
                            },
                        ) {
                            append(stringResource(Res.string.buying_me_a_coffee))
                        }
                        append("\n")
                        withLink(
                            LinkAnnotation.Url(
                                "https://www.linkedin.com/in/pabitra-banerjee",
                                TextLinkStyles(style = SpanStyle(textDecoration = TextDecoration.Underline, color = seed)),
                            ) {
                                onDoneReview.invoke()
                                onDismissRequest.invoke()
                                runCatching { openUrl("https://www.linkedin.com/in/pabitra-banerjee") }
                            },
                        ) {
                            append(stringResource(Res.string.linkedin))
                        }
                    },
                    textAlign = TextAlign.Center,
                    style = typo().bodySmall,
                )
            }
        },
    )
}