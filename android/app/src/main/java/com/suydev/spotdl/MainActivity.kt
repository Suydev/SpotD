package com.suydev.spotdl

import android.os.Bundle
import org.kivy.android.PythonActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : PythonActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize Python if not already done
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
    }
}
