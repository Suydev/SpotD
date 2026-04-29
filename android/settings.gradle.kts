pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url "https://chaquo.com/maven" }
    }
    plugins {
        id("com.chaquo.python") version "14.0.2"
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_PROJECT)
    repositories {
        google()
        mavenCentral()
        maven { url "https://chaquo.com/maven" }
    }
}

rootProject.name = "SpotDL"
include(":app")
