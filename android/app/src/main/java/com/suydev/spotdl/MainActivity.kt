package com.suydev.spotdl

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.suydev.spotdl.databinding.ActivityMainBinding
import org.python.util.PythonInterpreter
import org.python.core.PyObject
import org.python.core.PySystemState

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Launch Kivy app instead of WebView
        launchKivyApp()
    }

    private fun launchKivyApp() {
        // Start the Kivy app using Chaquopy
        val thread = Thread({
            try {
                // Initialize Python interpreter if not already done
                val interpreter = PythonInterpreter()
                interpreter.exec("import sys")

                // Add our Python directory to the path
                interpreter.exec("sys.path.append('/data/user/0/com.suydev.spotdl/files/app/src/main/python')")
                interpreter.exec("sys.path.append('/data/user/0/com.suydev.spotdl/files/app/src/main')")

                // Import and run the Kivy app
                interpreter.exec("""
                    from main import SpotDLApp
                    app = SpotDLApp()
                    app.run()
                """)

            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(
                        this@MainActivity,
                        "Failed to start Kivy app: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        })
        thread.start()
    }
}
