# 🎤 Multilingual Speech-to-Text with Sarvam AI

A Python application that converts speech to text in multiple Indian languages using Sarvam AI's powerful speech recognition API.

## 🌟 Features

- **Multilingual Support**: Supports 11 Indian languages + English
  - Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada
  - Malayalam, Marathi, Punjabi, Odia, English
- **Real-time Recording**: Record audio directly from your microphone
- **File Upload**: Upload pre-recorded audio files (WAV, MP3, M4A, FLAC)
- **Auto Language Detection**: Automatically detect the language being spoken
- **User-friendly GUI**: Clean and intuitive interface built with Tkinter
- **Copy to Clipboard**: Easy text copying functionality

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Sarvam AI API key ([Get one here](https://www.sarvam.ai/))
- Microphone (for real-time recording)

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   - Copy `.env.example` to `.env`
   - Add your Sarvam AI API key:
     ```
     SARVAM_API_KEY=your_api_key_here
     ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## 📱 How to Use

### Real-time Recording
1. Select your preferred language (or use "Auto-detect")
2. Click "🎙️ Start Recording"
3. Speak into your microphone
4. Click "⏹️ Stop Recording" when finished
5. View the transcribed text in the output area

### File Upload
1. Click "📁 Upload Audio File"
2. Select your audio file
3. Wait for processing
4. View the transcribed text

### Additional Features
- **Clear**: Remove all transcribed text
- **Copy Text**: Copy transcriptions to clipboard
- **Language Selection**: Choose specific language or auto-detect

## 🔧 Configuration

Edit `config.py` to modify:
- Audio recording settings (sample rate, channels, etc.)
- Supported languages
- API endpoints

## 📋 Supported Languages

| Language | Code |
|----------|------|
| Hindi | hi-IN |
| Bengali | bn-IN |
| Tamil | ta-IN |
| Telugu | te-IN |
| Gujarati | gu-IN |
| Kannada | kn-IN |
| Malayalam | ml-IN |
| Marathi | mr-IN |
| Punjabi | pa-IN |
| Odia | od-IN |
| English | en-IN |

## 🛠️ Advanced Features

### Speaker Diarization
For multiple speakers, you can use the diarization feature:

```python
from sarvam_client import SarvamSTT

stt = SarvamSTT()
result = stt.transcribe_with_diarization(
    "audio_file.wav", 
    language_code="hi-IN", 
    num_speakers=2
)
```

### Command Line Usage
You can also use the components programmatically:

```python
from audio_recorder import AudioRecorder
from sarvam_client import SarvamSTT

# Record audio
recorder = AudioRecorder()
recorder.start_recording()
# ... speak ...
recorder.stop_recording()
audio_file = recorder.save_audio("my_recording.wav")

# Transcribe
stt = SarvamSTT()
result = stt.transcribe_audio(audio_file, language_code="hi-IN")
print(result['transcript'])
```

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - On Windows: `pip install pyaudio`
   - On macOS: `brew install portaudio && pip install pyaudio`
   - On Linux: `sudo apt-get install portaudio19-dev && pip install pyaudio`

2. **"API key not found"**
   - Ensure you've created the `.env` file
   - Verify your API key is correct
   - Check that the file is in the same directory as `main.py`

3. **"Permission denied" for microphone**
   - Grant microphone permissions to your terminal/Python
   - Try running as administrator (Windows) or with sudo (Linux/macOS)

4. **Audio quality issues**
   - Ensure good microphone quality
   - Speak clearly and at moderate pace
   - Minimize background noise

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For API-related issues, contact [Sarvam AI Support](https://www.sarvam.ai/)
For application issues, please create an issue in this repository.
