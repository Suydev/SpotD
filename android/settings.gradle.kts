pluginManagement {
    repositories {
        maven { url "https://chaquo.com/maven" }
        google()
        mavenCentral()
        gradlePluginPortal()
    }
    plugins {
        id("com.chaquo.python") version "14.0.2"
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_PROJECT)
    repositories {
        maven { url "https://chaquo.com/maven" }
        google()
        mavenCentral()
    }
}

rootProject.name = "SpotDL"
include(":app")
