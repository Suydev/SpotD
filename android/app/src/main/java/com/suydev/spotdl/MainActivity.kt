package com.suydev.spotdl

import android.Manifest
import android.app.DownloadManager
import android.content.Context
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.view.KeyEvent
import android.view.View
import android.view.WindowManager
import android.webkit.CookieManager
import android.webkit.URLUtil
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.suydev.spotdl.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var web:     WebView
    private lateinit var refresh: SwipeRefreshLayout

    private val notifPermLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { /* no-op */ }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Match the app's dark theme — keep the status bar dark too.
        window.setBackgroundDrawable(null)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        web     = binding.web
        refresh = binding.refresh

        setupWebView()
        registerBackHandler()
        requestNotificationsIfNeeded()

        val startUrl = getString(R.string.server_url)
        web.loadUrl(startUrl)
    }

    private fun setupWebView() {
        with(web.settings) {
            javaScriptEnabled            = true
            domStorageEnabled            = true
            databaseEnabled              = true
            loadsImagesAutomatically     = true
            mediaPlaybackRequiresUserGesture = false
            cacheMode                    = WebSettings.LOAD_DEFAULT
            useWideViewPort              = true
            loadWithOverviewMode         = true
            mixedContentMode             = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
            userAgentString              = "$userAgentString SpotDL-Android/1.0"
            setSupportMultipleWindows(false)
            javaScriptCanOpenWindowsAutomatically = true
            allowFileAccess              = true
            allowContentAccess           = true
        }

        CookieManager.getInstance().setAcceptCookie(true)
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, true)

        web.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                refresh.isRefreshing = false
            }
            override fun onReceivedError(
                view: WebView?, request: WebResourceRequest?, error: WebResourceError?
            ) {
                refresh.isRefreshing = false
                if (request?.isForMainFrame == true) {
                    Toast.makeText(
                        this@MainActivity,
                        "Connection failed. Pull to retry.",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
            override fun shouldOverrideUrlLoading(
                view: WebView?, request: WebResourceRequest?
            ): Boolean {
                val url = request?.url?.toString() ?: return false
                // Open external links (mailto, tel, market, etc.) in the system handler.
                if (!url.startsWith("http")) {
                    return try {
                        startActivity(android.content.Intent(
                            android.content.Intent.ACTION_VIEW, Uri.parse(url)
                        )); true
                    } catch (e: Exception) { false }
                }
                return false
            }
        }
        web.webChromeClient = WebChromeClient()

        // File downloads → Android DownloadManager → /Music/SpotDL/
        web.setDownloadListener { url, userAgent, contentDisposition, mimeType, _ ->
            try {
                val fileName = URLUtil.guessFileName(url, contentDisposition, mimeType)
                val req = DownloadManager.Request(Uri.parse(url)).apply {
                    setMimeType(mimeType)
                    addRequestHeader("User-Agent", userAgent)
                    addRequestHeader("Cookie", CookieManager.getInstance().getCookie(url) ?: "")
                    setTitle(fileName)
                    setDescription("Saving from SpotDL")
                    setNotificationVisibility(
                        DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED
                    )
                    setAllowedOverMetered(true)
                    setAllowedOverRoaming(true)
                    val subdir = if (fileName.endsWith(".mp4", true)) "Movies/SpotDL"
                                 else "Music/SpotDL"
                    setDestinationInExternalPublicDir(subdir, fileName)
                }
                val dm = getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
                dm.enqueue(req)
                Toast.makeText(
                    this, "Downloading $fileName…", Toast.LENGTH_SHORT
                ).show()
            } catch (e: Exception) {
                Toast.makeText(
                    this, "Download failed: ${e.message}", Toast.LENGTH_LONG
                ).show()
            }
        }

        refresh.setOnRefreshListener { web.reload() }
        refresh.setColorSchemeColors(0xFF66E0CF.toInt(), 0xFFCDFFD0.toInt())
    }

    private fun registerBackHandler() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (web.canGoBack()) web.goBack() else { isEnabled = false; onBackPressedDispatcher.onBackPressed() }
            }
        })
    }

    private fun requestNotificationsIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val granted = ContextCompat.checkSelfPermission(
                this, Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
            if (!granted) notifPermLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }
}
