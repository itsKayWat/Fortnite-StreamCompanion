import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import pygame  # Add for sound effects
from tkinter import filedialog
import cv2  # Add for VOD review

class FortniteCompanion:
    def __init__(self):
        try:
            # Initialize main window
            self.root = tk.Tk()
            self.root.title("Fortnite Stream Tools")
            self.root.geometry("1000x800")
            
            self.colors = {
                'bg': '#121212',
                'fg': '#FFFFFF',
                'success': '#00FF00',
                'danger': '#FF4444',
                'accent': '#9147FF',
                'warning': '#FFA500',
                'secondary': '#2D2D2D',
                'highlight': '#3F3F3F'
            }
            
            self.root.configure(bg=self.colors['bg'])
            
            # Initialize basic variables
            self.elim_count = tk.IntVar(value=0)
            self.stats = {}  # Initialize empty before loading
            try:
                self.stats = self.load_stats()
            except:
                print("Warning: Could not load stats")
            
            self.session_start = datetime.now()
            
            # Initialize feature variables
            self.replay_buffer = []
            self.stream_connected = False
            self.sound_effects = None
            self.current_vod = None
            
            # Try to initialize pygame
            try:
                pygame.mixer.init()
                self.sound_effects = {}
                self.load_sound_effects()
            except Exception as e:
                print(f"Warning: Sound system initialization failed: {e}")
                self.sound_effects = None
            
            # Create UI elements
            try:
                self.create_notebook()
                self.create_tabs()
            except Exception as e:
                print(f"Error creating UI: {e}")
                raise
            
        except Exception as e:
            print(f"Critical initialization error: {e}")
            raise

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

    def create_tabs(self):
        # Create all frames
        self.main_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.quick_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.polls_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.predictions_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.stats_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.tournament_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.challenges_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.overlay_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.stream_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.replay_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.vod_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.scrim_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        
        # Add frames to notebook
        self.notebook.add(self.main_frame, text='Main')
        self.notebook.add(self.quick_frame, text='Quick Actions')
        self.notebook.add(self.polls_frame, text='Polls')
        self.notebook.add(self.predictions_frame, text='Predictions')
        self.notebook.add(self.stats_frame, text='Stats')
        self.notebook.add(self.tournament_frame, text='Tournament')
        self.notebook.add(self.challenges_frame, text='Challenges')
        self.notebook.add(self.overlay_frame, text='Overlays')
        self.notebook.add(self.stream_frame, text='Stream')
        self.notebook.add(self.replay_frame, text='Replays')
        self.notebook.add(self.vod_frame, text='VOD Review')
        self.notebook.add(self.scrim_frame, text='Scrims')
        
        # Setup each tab
        self.setup_main_tab()
        self.setup_quick_actions()
        self.setup_polls_tab()
        self.setup_predictions_tab()
        self.setup_stats_tab()
        self.setup_tournament_tab()
        self.setup_challenges_tab()
        self.setup_overlay_tab()
        self.setup_stream_tab()
        self.setup_replay_tab()
        self.setup_vod_tab()
        self.setup_scrim_tab()

    def create_button(self, parent, text, command, color=None, size="normal"):
        if color is None:
            color = self.colors['accent']
        
        font_size = 16 if size == "large" else 12
        
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Arial', font_size),
            relief=tk.RAISED,
            borderwidth=2
        )

    def setup_main_tab(self):
        # Victory Button
        victory_btn = self.create_button(
            self.main_frame,
            "🏆 VICTORY ROYALE! 🏆",
            self.record_victory,
            self.colors['success'],
            "large"
        )
        victory_btn.pack(pady=20, padx=20, fill='x')
        
        # Eliminations Counter
        elim_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        elim_frame.pack(pady=10)
        
        self.create_button(
            elim_frame,
            "-",
            lambda: self.update_elims(-1),
            self.colors['danger']
        ).pack(side='left', padx=5)
        
        tk.Label(
            elim_frame,
            textvariable=self.elim_count,
            bg=self.colors['bg'],
            fg='white',
            font=('Arial', 24, 'bold'),
            width=5
        ).pack(side='left')
        
        self.create_button(
            elim_frame,
            "+",
            lambda: self.update_elims(1),
            self.colors['success']
        ).pack(side='left', padx=5)

    def setup_quick_actions(self):
        actions = [
            ("Start New Game", self.start_new_game),
            ("Mark Top 10", self.mark_top_10),
            ("Reset Session", self.reset_session),
            ("Save Clip", self.save_clip),
            ("Toggle Overlay", self.toggle_overlay)
        ]
        
        for text, command in actions:
            self.create_button(
                self.quick_frame,
                text,
                command
            ).pack(pady=5, padx=20, fill='x')

    def setup_polls_tab(self):
        categories = {
            "Landing Spots": [
                "Tilted Towers", "Pleasant Park", "Retail Row",
                "Lazy Lake", "Random Drop", "Viewer Choice"
            ],
            "Loadout Challenge": [
                "Pistols Only", "No Building", "Snipers Only",
                "Common Weapons Only", "No Healing Items"
            ],
            "Stream Polls": [
                "One More Game?", "Need a Break?",
                "Squad Up with Viewers?", "Change Game Mode?"
            ]
        }
        
        for category, options in categories.items():
            frame = tk.LabelFrame(
                self.polls_frame,
                text=category,
                bg=self.colors['bg'],
                fg='white'
            )
            frame.pack(pady=5, padx=10, fill='x')
            
            for option in options:
                self.create_button(
                    frame,
                    option,
                    lambda o=option: self.start_poll(o)
                ).pack(pady=2, padx=10, fill='x')

    def setup_predictions_tab(self):
        categories = {
            "Game Predictions": [
                "Victory This Game?", "Top 5 Finish?",
                "10+ Eliminations?", "Find Legendary Weapon?"
            ],
            "Session Goals": [
                "3+ Wins Today?", "20+ Kill Game?",
                "New Personal Record?", "Complete Challenge?"
            ]
        }
        
        for category, options in categories.items():
            frame = tk.LabelFrame(
                self.predictions_frame,
                text=category,
                bg=self.colors['bg'],
                fg='white'
            )
            frame.pack(pady=5, padx=10, fill='x')
            
            for option in options:
                self.create_button(
                    frame,
                    option,
                    lambda o=option: self.start_prediction(o)
                ).pack(pady=2, padx=10, fill='x')
        
        # Custom prediction
        custom_frame = tk.LabelFrame(
            self.predictions_frame,
            text="Custom Prediction",
            bg=self.colors['bg'],
            fg='white'
        )
        custom_frame.pack(pady=5, padx=10, fill='x')
        
        self.pred_entry = tk.Entry(
            custom_frame,
            bg='white',
            fg='black',
            font=('Arial', 12)
        )
        self.pred_entry.pack(pady=5, padx=10, fill='x')
        
        self.create_button(
            custom_frame,
            "Start Custom Prediction",
            self.start_custom_prediction
        ).pack(pady=5, padx=10, fill='x')

    def setup_stats_tab(self):
        # Session Stats
        session_frame = tk.LabelFrame(
            self.stats_frame,
            text="Session Statistics",
            bg=self.colors['bg'],
            fg='white'
        )
        session_frame.pack(pady=5, padx=10, fill='x')
        
        self.session_stats = {
            'Victories': tk.StringVar(value="0"),
            'Eliminations': tk.StringVar(value="0"),
            'Games Played': tk.StringVar(value="0"),
            'K/D Ratio': tk.StringVar(value="0.0"),
            'Win Rate': tk.StringVar(value="0%"),
            'Top 10s': tk.StringVar(value="0")
        }
        
        for stat, var in self.session_stats.items():
            frame = tk.Frame(session_frame, bg=self.colors['bg'])
            frame.pack(fill='x', pady=2)
            
            tk.Label(
                frame,
                text=f"{stat}:",
                bg=self.colors['bg'],
                fg='white'
            ).pack(side='left', padx=5)
            
            tk.Label(
                frame,
                textvariable=var,
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(side='right', padx=5)

    def setup_tournament_tab(self):
        # Tournament controls
        controls_frame = tk.LabelFrame(
            self.tournament_frame,
            text="Tournament Controls",
            bg=self.colors['bg'],
            fg='white'
        )
        controls_frame.pack(pady=5, padx=10, fill='x')
        
        tournament_types = [
            "Solo Cash Cup",
            "Duo Arena",
            "Trio Tournament",
            "Squad Scrims"
        ]
        
        for t_type in tournament_types:
            self.create_button(
                controls_frame,
                t_type,
                lambda t=t_type: self.start_tournament(t)
            ).pack(pady=2, padx=10, fill='x')

    def setup_challenges_tab(self):
        challenge_types = {
            "Combat Challenges": [
                "No Building", "Pistols Only", "No Healing",
                "Common Weapons", "Sniper Only"
            ],
            "Movement Challenges": [
                "No Running", "Must Crouch", "No Vehicles",
                "Water Travel Only", "Must Dance After Kills"
            ],
            "Strategy Challenges": [
                "Edge of Storm", "One POI Only", "No Farming",
                "Random Loadout", "First Weapons Only"
            ]
        }
        
        for category, challenges in challenge_types.items():
            frame = tk.LabelFrame(
                self.challenges_frame,
                text=category,
                bg=self.colors['bg'],
                fg='white'
            )
            frame.pack(pady=5, padx=10, fill='x')
            
            for challenge in challenges:
                self.create_button(
                    frame,
                    challenge,
                    lambda c=challenge: self.start_challenge(c)
                ).pack(pady=2, padx=10, fill='x')

    def setup_overlay_tab(self):
        overlay_types = [
            "Tournament Overlay",
            "Stats Display",
            "Victory Counter",
            "Challenge Timer",
            "Custom Text"
        ]
        
        for overlay in overlay_types:
            self.create_button(
                self.overlay_frame,
                overlay,
                lambda o=overlay: self.toggle_overlay_type(o)
            ).pack(pady=5, padx=20, fill='x')

    def setup_stream_tab(self):
        # Stream integration controls
        controls = [
            ("Connect to Twitch", self.connect_stream),
            ("Start Poll", self.quick_stream_poll),
            ("Channel Points Reward", self.manage_channel_points),
            ("Chat Commands", self.setup_chat_commands)
        ]
        
        for text, command in controls:
            self.create_button(
                self.stream_frame,
                text,
                command
            ).pack(pady=5, padx=20, fill='x')

    def setup_replay_tab(self):
        # Match replay controls
        controls_frame = tk.LabelFrame(
            self.replay_frame,
            text="Match Replay Controls",
            bg=self.colors['bg'],
            fg='white'
        )
        controls_frame.pack(pady=5, padx=10, fill='x')
        
        actions = [
            ("Start Recording", self.start_replay_recording),
            ("Save Last Match", self.save_replay),
            ("View Replays", self.view_replays),
            ("Export Highlight", self.export_highlight)
        ]
        
        for text, command in actions:
            self.create_button(
                controls_frame,
                text,
                command
            ).pack(pady=2, padx=10, fill='x')

    def setup_vod_tab(self):
        # VOD review tools
        controls = [
            ("Load VOD", self.load_vod),
            ("Add Timestamp", self.add_timestamp),
            ("Export Notes", self.export_vod_notes),
            ("Analysis Tools", self.show_analysis_tools)
        ]
        
        for text, command in controls:
            self.create_button(
                self.vod_frame,
                text,
                command
            ).pack(pady=5, padx=20, fill='x')

    def setup_scrim_tab(self):
        # Scrim practice controls
        scrim_types = {
            "Practice Modes": [
                "Box Fighting",
                "Build Battles",
                "Zone Wars",
                "Realistic 1v1"
            ],
            "Team Scrims": [
                "Duo Scrims",
                "Trio Arena",
                "Squad Custom"
            ]
        }
        
        for category, options in scrim_types.items():
            frame = tk.LabelFrame(
                self.scrim_frame,
                text=category,
                bg=self.colors['bg'],
                fg='white'
            )
            frame.pack(pady=5, padx=10, fill='x')
            
            for option in options:
                self.create_button(
                    frame,
                    option,
                    lambda o=option: self.start_scrim(o)
                ).pack(pady=2, padx=10, fill='x')

    # Event handlers
    def update_elims(self, delta):
        new_value = self.elim_count.get() + delta
        if new_value >= 0:
            self.elim_count.set(new_value)
            self.update_stats()

    def record_victory(self):
        self.stats['victories'] = self.stats.get('victories', 0) + 1
        self.save_stats()
        self.update_stats()
        
        popup = tk.Toplevel(self.root)
        popup.geometry("300x200")
        popup.configure(bg=self.colors['success'])
        
        tk.Label(
            popup,
            text="VICTORY ROYALE!",
            bg=self.colors['success'],
            fg='black',
            font=('Arial', 24, 'bold')
        ).pack(expand=True)
        
        popup.after(3000, popup.destroy)

    def start_poll(self, question):
        popup = tk.Toplevel(self.root)
        popup.geometry("400x300")
        popup.configure(bg=self.colors['bg'])
        popup.title("Poll")
        
        tk.Label(
            popup,
            text=question,
            bg=self.colors['bg'],
            fg='white',
            font=('Arial', 16)
        ).pack(pady=20)
        
        options_frame = tk.Frame(popup, bg=self.colors['bg'])
        options_frame.pack(expand=True)
        
        for option in ["Yes", "No"]:
            self.create_button(
                options_frame,
                option,
                popup.destroy
            ).pack(side=tk.LEFT, padx=10)

    def start_prediction(self, question):
        popup = tk.Toplevel(self.root)
        popup.geometry("400x300")
        popup.configure(bg=self.colors['bg'])
        popup.title("Prediction")
        
        tk.Label(
            popup,
            text=question,
            bg=self.colors['bg'],
            fg='white',
            font=('Arial', 16)
        ).pack(pady=20)
        
        options_frame = tk.Frame(popup, bg=self.colors['bg'])
        options_frame.pack(expand=True)
        
        for option in ["Yes", "No"]:
            self.create_button(
                options_frame,
                option,
                popup.destroy
            ).pack(side=tk.LEFT, padx=10)

    def start_custom_prediction(self):
        if self.pred_entry.get().strip():
            self.start_prediction(self.pred_entry.get())
            self.pred_entry.delete(0, tk.END)

    def start_new_game(self):
        self.elim_count.set(0)
        self.stats['games_played'] = self.stats.get('games_played', 0) + 1
        self.save_stats()
        self.update_stats()

    def mark_top_10(self):
        self.stats['top_10s'] = self.stats.get('top_10s', 0) + 1
        self.save_stats()
        self.update_stats()
        
        popup = tk.Toplevel(self.root)
        popup.geometry("300x200")
        popup.configure(bg=self.colors['warning'])
        
        tk.Label(
            popup,
            text="TOP 10!",
            bg=self.colors['warning'],
            fg='black',
            font=('Arial', 24, 'bold')
        ).pack(expand=True)
        
        popup.after(2000, popup.destroy)

    def reset_session(self):
        self.stats = {'victories': 0, 'eliminations': 0, 'games_played': 0, 'top_10s': 0}
        self.elim_count.set(0)
        self.save_stats()
        self.update_stats()

    def save_clip(self):
        # Placeholder for clip saving functionality
        pass

    def toggle_overlay(self):
        # Placeholder for overlay toggle functionality
        pass

    def start_tournament(self, t_type):
        # Placeholder for tournament functionality
        pass

    def start_challenge(self, challenge):
        popup = tk.Toplevel(self.root)
        popup.geometry("400x200")
        popup.configure(bg=self.colors['bg'])
        
        tk.Label(
            popup,
            text=f"Challenge Started:\n{challenge}",
            bg=self.colors['bg'],
            fg='white',
            font=('Arial', 16)
        ).pack(expand=True)
        
        popup.after(3000, popup.destroy)

    def connect_stream(self):
        # Placeholder for stream connection logic
        self.stream_connected = not self.stream_connected
        status = "Connected" if self.stream_connected else "Disconnected"
        messagebox.showinfo("Stream Status", f"Stream {status}")

    def start_scrim(self, scrim_type):
        # Placeholder for scrim functionality
        messagebox.showinfo("Scrim Started", f"Starting {scrim_type} scrim mode")

    def load_vod(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv")]
        )
        if file_path:
            self.current_vod = file_path
            messagebox.showinfo("VOD Loaded", "VOD file loaded successfully")

    def load_sound_effects(self):
        # Load common sound effects
        sound_files = {
            'victory': 'sounds/victory.wav',
            'elimination': 'sounds/elim.wav',
            'death': 'sounds/death.wav'
        }
        
        for name, file in sound_files.items():
            try:
                self.sound_effects[name] = pygame.mixer.Sound(file)
            except:
                print(f"Could not load sound effect: {file}")

    def play_sound(self, sound_name):
        if self.sound_effects is None:
            return
        if sound_name in self.sound_effects:
            try:
                self.sound_effects[sound_name].play()
            except:
                print(f"Warning: Could not play sound {sound_name}")

    def run(self):
        self.root.mainloop()

    def load_stats(self):
        try:
            with open('stats.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("No existing stats file found, creating new one")
            return {'victories': 0, 'eliminations': 0, 'games_played': 0, 'top_10s': 0}
        except Exception as e:
            print(f"Error loading stats: {e}")
            return {'victories': 0, 'eliminations': 0, 'games_played': 0, 'top_10s': 0}

    def quick_stream_poll(self):
        # Placeholder for stream poll functionality
        messagebox.showinfo("Stream Poll", "Starting quick stream poll...")

    def manage_channel_points(self):
        # Placeholder for channel points management
        messagebox.showinfo("Channel Points", "Opening channel points manager...")

    def setup_chat_commands(self):
        # Placeholder for chat commands setup
        messagebox.showinfo("Chat Commands", "Opening chat commands setup...")

    def start_replay_recording(self):
        # Placeholder for replay recording
        messagebox.showinfo("Replay", "Starting replay recording...")

    def save_replay(self):
        # Placeholder for replay saving
        messagebox.showinfo("Replay", "Saving replay...")

    def view_replays(self):
        # Placeholder for replay viewing
        messagebox.showinfo("Replay", "Opening replay viewer...")

    def export_highlight(self):
        # Placeholder for highlight export
        messagebox.showinfo("Replay", "Exporting highlight...")

    def add_timestamp(self):
        # Placeholder for VOD timestamp
        messagebox.showinfo("VOD Review", "Adding timestamp...")

    def export_vod_notes(self):
        # Placeholder for VOD notes export
        messagebox.showinfo("VOD Review", "Exporting VOD notes...")

    def show_analysis_tools(self):
        # Placeholder for analysis tools
        messagebox.showinfo("VOD Review", "Opening analysis tools...")

if __name__ == "__main__":
    app = FortniteCompanion()
    app.run()