import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from audio_recorder import AudioRecorder
from sarvam_client import SarvamSTT
from config import SUPPORTED_LANGUAGES

class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multilingual Speech-to-Text with Sarvam AI")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        try:
            self.recorder = AudioRecorder()
            self.audio_available = True
        except ImportError:
            self.recorder = None
            self.audio_available = False
            
        self.stt_client = SarvamSTT()
        self.is_recording = False
        
        # Setup GUI
        self.setup_ui()
        
        # Cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_label = tk.Label(
            self.root, 
            text="🎤 Multilingual Speech-to-Text", 
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(20, 10))
        
        # Language selection frame
        lang_frame = tk.Frame(self.root, bg='#f0f0f0')
        lang_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            lang_frame, 
            text="Select Language:", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.language_var = tk.StringVar(value="Auto-detect")
        self.language_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=list(SUPPORTED_LANGUAGES.keys()),
            state="readonly",
            width=15,
            font=('Arial', 11)
        )
        self.language_combo.pack(side='left', padx=(10, 0))
        
        # Translate to English option
        self.translate_var = tk.BooleanVar(value=True)  # Default to True for English output
        self.translate_checkbox = tk.Checkbutton(
            lang_frame,
            text="Output in English",
            variable=self.translate_var,
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        self.translate_checkbox.pack(side='left', padx=(20, 0))
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=20)
        
        self.record_btn = tk.Button(
            control_frame,
            text="🎙️ Start Recording" if self.audio_available else "🎙️ Recording Disabled",
            command=self.toggle_recording if self.audio_available else self.show_audio_warning,
            font=('Arial', 12, 'bold'),
            bg='#27ae60' if self.audio_available else '#95a5a6',
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            borderwidth=2,
            state='normal' if self.audio_available else 'disabled'
        )
        self.record_btn.pack(side='left', padx=10)
        
        self.upload_btn = tk.Button(
            control_frame,
            text="📁 Upload Audio File",
            command=self.upload_audio_file,
            font=('Arial', 12),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            borderwidth=2
        )
        self.upload_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear",
            command=self.clear_output,
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            borderwidth=2
        )
        self.clear_btn.pack(side='left', padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to record...",
            font=('Arial', 11),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=(10, 0))
        
        # Output text area
        output_frame = tk.Frame(self.root, bg='#f0f0f0')
        output_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        tk.Label(
            output_frame,
            text="📝 Transcribed Text:",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='white',
            fg='#2c3e50',
            relief='sunken',
            borderwidth=2,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Copy button
        copy_btn = tk.Button(
            output_frame,
            text="📋 Copy Text",
            command=self.copy_text,
            font=('Arial', 10),
            bg='#95a5a6',
            fg='white',
            padx=15,
            pady=5
        )
        copy_btn.pack(pady=(10, 0))
        
        # Info label
        info_label = tk.Label(
            self.root,
            text="✨ NEW: Check 'Output in English' to get English translation regardless of spoken language!\n"
                 "Supports: Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia, English",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#7f8c8d',
            wraplength=750
        )
        info_label.pack(pady=(0, 10))
    
    def toggle_recording(self):
        """Toggle audio recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start audio recording"""
        try:
            if self.recorder.start_recording():
                self.is_recording = True
                self.record_btn.config(
                    text="⏹️ Stop Recording",
                    bg='#e74c3c'
                )
                self.status_label.config(
                    text="🔴 Recording... Click 'Stop Recording' when finished",
                    fg='#e74c3c'
                )
                self.upload_btn.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
    
    def stop_recording(self):
        """Stop audio recording and process"""
        if self.is_recording:
            self.is_recording = False
            self.record_btn.config(
                text="🎙️ Start Recording",
                bg='#27ae60'
            )
            self.status_label.config(
                text="⏳ Processing audio...",
                fg='#f39c12'
            )
            self.upload_btn.config(state='normal')
            
            # Process recording in a separate thread
            threading.Thread(target=self.process_recorded_audio, daemon=True).start()
    
    def process_recorded_audio(self):
        """Process the recorded audio"""
        try:
            # Stop recording and save to file
            frames = self.recorder.stop_recording()
            if frames:
                audio_file = self.recorder.save_audio("temp_recording.wav")
                self.transcribe_audio(audio_file)
                
                # Clean up temporary file
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="❌ No audio recorded",
                    fg='#e74c3c'
                ))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to process recording: {str(e)}"))
    
    def upload_audio_file(self):
        """Upload and process an audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.flac"),
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.status_label.config(
                text="⏳ Processing uploaded file...",
                fg='#f39c12'
            )
            # Process in separate thread
            threading.Thread(target=lambda: self.transcribe_audio(file_path), daemon=True).start()
    
    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using Sarvam AI"""
        try:
            # Get selected language and translation preference
            selected_lang = self.language_var.get()
            language_code = SUPPORTED_LANGUAGES.get(selected_lang, "unknown")
            translate_to_english = self.translate_var.get()
            
            # Call Sarvam AI API
            result = self.stt_client.transcribe_audio(
                audio_file_path, 
                language_code, 
                translate_to_english=translate_to_english
            )
            
            # Update UI in main thread
            self.root.after(0, lambda: self.display_result(result))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Transcription failed: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(
                text="❌ Transcription failed",
                fg='#e74c3c'
            ))
    
    def display_result(self, result):
        """Display transcription result"""
        if result['success']:
            transcript = result['transcript']
            if transcript.strip():
                # Add timestamp and language info
                if result.get('translated_to_english', False):
                    source_lang = result.get('source_language', result.get('language_detected', 'unknown'))
                    display_text = f"🌐 [{source_lang} → English] {transcript}\n"
                else:
                    lang_detected = result.get('language_detected', 'unknown')
                    display_text = f"📝 [{lang_detected}] {transcript}\n"
                
                confidence = result.get('confidence', 0)
                if confidence > 0:
                    display_text += f"(Confidence: {confidence:.2f})\n"
                display_text += "\n" + "="*50 + "\n\n"
                
                # Insert at the beginning
                self.output_text.insert('1.0', display_text)
                
                self.status_label.config(
                    text="✅ Transcription completed successfully!",
                    fg='#27ae60'
                )
            else:
                self.status_label.config(
                    text="⚠️ No speech detected in audio",
                    fg='#f39c12'
                )
        else:
            error_msg = result.get('error', 'Unknown error')
            messagebox.showerror("Transcription Error", error_msg)
            self.status_label.config(
                text="❌ Transcription failed",
                fg='#e74c3c'
            )
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete('1.0', tk.END)
        self.status_label.config(
            text="Ready to record...",
            fg='#7f8c8d'
        )
    
    def copy_text(self):
        """Copy text to clipboard"""
        try:
            text = self.output_text.get('1.0', tk.END).strip()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.status_label.config(
                    text="📋 Text copied to clipboard!",
                    fg='#27ae60'
                )
            else:
                self.status_label.config(
                    text="⚠️ No text to copy",
                    fg='#f39c12'
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {str(e)}")
    
    def show_audio_warning(self):
        """Show warning when audio recording is not available"""
        messagebox.showwarning(
            "Audio Recording Unavailable",
            "Audio recording is not available because PyAudio is not installed.\n\n"
            "To enable audio recording:\n"
            "1. Install PyAudio: pip install PyAudio\n"
            "2. Restart the application\n\n"
            "You can still upload audio files for transcription."
        )
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_recording and self.recorder:
            self.recorder.stop_recording()
        
        if self.recorder:
            self.recorder.cleanup()
        self.root.destroy()

def main():
    """Main function to run the application"""
    # Check if API key is configured
    from config import SARVAM_API_KEY
    if not SARVAM_API_KEY:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Configuration Error",
            "Sarvam API key not found!\n\n"
            "Please:\n"
            "1. Copy .env.example to .env\n"
            "2. Add your Sarvam AI API key to the .env file\n"
            "3. Restart the application"
        )
        return
    
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
