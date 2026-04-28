import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import mainthread
import threading
import requests
import json
import os
from urllib.parse import quote_plus

# Set window size for mobile-like behavior during development
if platform != 'android':
    Window.size = (400, 700)

class SpotDLApp(App):
    def build(self):
        self.title = 'SpotDL'

        # Main layout
        main_layout = BoxLayout(orientation='vertical')

        # Create tabbed panel for different sections
        self.tab_panel = TabbedPanel(do_default_tab=False)

        # Add tabs
        self.tab_panel.add_widget(self.create_search_tab())
        self.tab_panel.add_widget(self.create_downloads_tab())
        self.tab_panel.add_widget(self.create_settings_tab())

        main_layout.add_widget(self.tab_panel)
        return main_layout

    def create_search_tab(self):
        tab = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = Label(
            text='SpotDL - Spotify & YouTube Downloader',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        tab.add_widget(header)

        # Search input
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.search_input = TextInput(
            hint_text='Enter Spotify URL or search...',
            multiline=False,
            size_hint_x=0.7
        )
        search_button = Button(
            text='Search',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        search_button.bind(on_press=self.perform_search)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        tab.add_widget(search_layout)

        # Results area
        results_label = Label(
            text='Search Results:',
            size_hint_y=None,
            height=30,
            halign='left',
            bold=True
        )
        tab.add_widget(results_label)

        self.results_scroll = ScrollView()
        self.results_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        tab.add_widget(self.results_scroll)

        return tab

    def create_downloads_tab(self):
        tab = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = Label(
            text='Active Downloads',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        tab.add_widget(header)

        # Downloads list
        self.downloads_scroll = ScrollView()
        self.downloads_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.downloads_layout.bind(minimum_height=self.downloads_layout.setter('height'))
        self.downloads_scroll.add_widget(self.downloads_layout)
        tab.add_widget(self.downloads_scroll)

        return tab

    def create_settings_tab(self):
        tab = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = Label(
            text='Settings',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        tab.add_widget(header)

        # Settings form
        settings_form = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        settings_form.bind(minimum_height=settings_form.setter('height'))

        # Audio quality
        settings_form.add_widget(Label(text='Audio Quality:', halign='right', valign='middle'))
        self.audio_quality = TextInput(text='mp3-320', multiline=False)
        settings_form.add_widget(self.audio_quality)

        # Video quality
        settings_form.add_widget(Label(text='Video Quality:', halign='right', valign='middle'))
        self.video_quality = TextInput(text='720p', multiline=False)
        settings_form.add_widget(self.video_quality)

        # Max songs
        settings_form.add_widget(Label(text='Max Songs:', halign='right', valign='middle'))
        self.max_songs = TextInput(text='100', multiline=False, input_filter='int')
        settings_form.add_widget(self.max_songs)

        # Chunk size
        settings_form.add_widget(Label(text='Chunk Size:', halign='right', valign='middle'))
        self.chunk_size = TextInput(text='25', multiline=False, input_filter='int')
        settings_form.add_widget(self.chunk_size)

        tab.add_widget(settings_form)

        # Save button
        save_button = Button(
            text='Save Settings',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        save_button.bind(on_press=self.save_settings)
        tab.add_widget(save_button)

        return tab

    def perform_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            return

        # Show loading state
        self.show_loading_results("Searching...")

        # Perform search in background thread
        threading.Thread(target=self._perform_search_thread, args=(query,), daemon=True).start()

    def _perform_search_thread(self, query):
        try:
            # Call the Flask backend API
            response = requests.get(
                f'http://127.0.0.1:5000/api/search',
                params={'q': query, 'limit': 8},
                timeout=10
            )

            if response.status_code == 200:
                results = response.json()
                self.update_search_results(results)
            else:
                self.show_error_results(f"Search failed: {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.show_error_results("Cannot connect to backend. Is the server running?")
        except Exception as e:
            self.show_error_results(f"Error: {str(e)}")

    @mainthread
    def update_search_results(self, results):
        # Clear previous results
        self.results_layout.clear_widgets()

        # Add tracks
        if results.get('tracks'):
            tracks_label = Label(
                text='Tracks:',
                size_hint_y=None,
                height=30,
                halign='left',
                bold=True,
                font_size='16sp'
            )
            self.results_layout.add_widget(tracks_label)

            for track in results['tracks'][:5]:  # Limit to 5 for display
                track_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=5)
                track_layout.add_widget(Label(
                    text=f"{track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}",
                    size_hint_y=None,
                    height=30,
                    bold=True
                ))
                if track.get('album'):
                    track_layout.add_widget(Label(
                        text=f"Album: {track['album']}",
                        size_hint_y=None,
                        height=20,
                        font_size='12sp'
                    ))
                select_btn = Button(
                    text='Select',
                    size_hint_y=None,
                    height=30,
                    background_color=(0.2, 0.6, 0.8, 1)
                )
                select_btn.bind(on_press=lambda x, t=track: self.select_track(t))
                track_layout.add_widget(select_btn)
                self.results_layout.add_widget(track_layout)

        # Add playlists
        if results.get('playlists'):
            playlists_label = Label(
                text='Playlists:',
                size_hint_y=None,
                height=30,
                halign='left',
                bold=True,
                font_size='16sp'
            )
            self.results_layout.add_widget(playlists_label)

            for playlist in results['playlists'][:3]:  # Limit to 3 for display
                playlist_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=5)
                playlist_layout.add_widget(Label(
                    text=f"{playlist.get('name', 'Unknown')} - {playlist.get('artist', 'Unknown')}",
                    size_hint_y=None,
                    height=30,
                    bold=True
                ))
                if playlist.get('tracks_count'):
                    playlist_layout.add_widget(Label(
                        text=f"{playlist['tracks_count']} tracks",
                        size_hint_y=None,
                        height=20,
                        font_size='12sp'
                    ))
                select_btn = Button(
                    text='Select',
                    size_hint_y=None,
                    height=30,
                    background_color=(0.2, 0.6, 0.8, 1)
                )
                select_btn.bind(on_press=lambda x, p=playlist: self.select_playlist(p))
                playlist_layout.add_widget(select_btn)
                self.results_layout.add_widget(playlist_layout)

        # If no results
        if not results.get('tracks') and not results.get('playlists') and not results.get('albums'):
            no_results = Label(
                text='No results found',
                size_hint_y=None,
                height=40,
                halign='center'
            )
            self.results_layout.add_widget(no_results)

    @mainthread
    def show_loading_results(self, message):
        self.results_layout.clear_widgets()
        loading = Label(
            text=message,
            size_hint_y=None,
            height=40,
            halign='center'
        )
        self.results_layout.add_widget(loading)

    @mainthread
    def show_error_results(self, message):
        self.results_layout.clear_widgets()
        error_label = Label(
            text=message,
            size_hint_y=None,
            height=40,
            halign='center',
            color=(1, 0, 0, 1)
        )
        self.results_layout.add_widget(error_label)

    def select_track(self, track):
        # For now, just show a toast message
        # In a full implementation, this would start the download
        from kivy.toast import toast
        toast(f"Selected: {track.get('name', 'Unknown')}")

    def select_playlist(self, playlist):
        # For now, just show a toast message
        from kivy.toast import toast
        toast(f"Selected playlist: {playlist.get('name', 'Unknown')}")

    def save_settings(self, instance):
        # Save settings to shared preferences or file
        from kivy.toast import toast
        toast("Settings saved!")
        print(f"Audio quality: {self.audio_quality.text}")
        print(f"Video quality: {self.video_quality.text}")
        print(f"Max songs: {self.max_songs.text}")
        print(f"Chunk size: {self.chunk_size.text}")

if __name__ == '__main__':
    SpotDLApp().run()