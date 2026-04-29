// Top-level build file where you can add configuration options common to all sub-projects/modules.

plugins {
    // Apply the application plugin as a common plugin if needed
}

allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://chaquo.com/maven") }
    }
}