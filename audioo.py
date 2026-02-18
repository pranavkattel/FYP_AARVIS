import pyaudio
import wave
import threading
import queue
import time
import tempfile
import os
from faster_whisper import WhisperModel

class RealTimeTranscriber:
    def __init__(self, model_size="large-v3", device="cpu", compute_type="int8"):
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 2  # Process every 2 seconds
        
        # Initialize Whisper model with fallback
        print(f"Loading Whisper model: {model_size} on {device}")
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
            print(f"✅ Model loaded successfully on {device}")
        except Exception as e:
            print(f"❌ Error loading model on {device}: {e}")
            if device == "cuda":
                print("🔄 Falling back to CPU...")
                self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
                print("✅ Model loaded successfully on CPU")
            else:
                raise e
        
        # Audio recording setup
        self.audio = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
    def display_words_progressively(self, text, delay=0.15):
        """Display text word by word with a delay"""
        if not text:
            return
            
        words = text.split()
        timestamp = time.strftime("%H:%M:%S")
        print(f"\n[{timestamp}] ", end="", flush=True)
        
        for i, word in enumerate(words):
            print(f"{word}", end=" ", flush=True)
            time.sleep(delay)
        print()  # New line after sentence
        
    def audio_callback(self):
        """Continuously record audio and put it in queue"""
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        print("🎤 Listening... (Press Ctrl+C to stop)")
        
        while self.is_recording:
            frames = []
            for _ in range(int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                if not self.is_recording:
                    break
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
            
            if frames:
                self.audio_queue.put(frames)
        
        stream.stop_stream()
        stream.close()
    
    def transcribe_audio_chunk(self, frames):
        """Transcribe a chunk of audio frames and return word-level segments"""
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            wf = wave.open(temp_file.name, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            try:
                # Transcribe the audio chunk with word-level timestamps
                segments, info = self.model.transcribe(
                    temp_file.name, 
                    beam_size=5,
                    language="en",  # You can remove this to auto-detect language
                    word_timestamps=True  # Enable word-level timestamps
                )
                
                # Extract words with timestamps
                words_with_timing = []
                for segment in segments:
                    if hasattr(segment, 'words') and segment.words:
                        for word in segment.words:
                            words_with_timing.append({
                                'word': word.word,
                                'start': word.start,
                                'end': word.end,
                                'probability': word.probability if hasattr(word, 'probability') else 1.0
                            })
                    else:
                        # Fallback if word timestamps aren't available
                        text = segment.text.strip()
                        if text:
                            words_with_timing.append({
                                'word': text,
                                'start': segment.start,
                                'end': segment.end,
                                'probability': 1.0
                            })
                
                return words_with_timing
                
            except Exception as e:
                print(f"Transcription error: {e}")
                return []
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
    
    def start_transcription(self):
        """Start real-time transcription"""
        self.is_recording = True
        
        # Start audio recording thread
        audio_thread = threading.Thread(target=self.audio_callback)
        audio_thread.daemon = True
        audio_thread.start()
        
        print("🚀 Real-time transcription started!")
        print("📝 Words will appear one by one as they are recognized:")
        print("-" * 60)
        
        current_line = ""
        
        try:
            while self.is_recording:
                try:
                    # Get audio chunk from queue
                    frames = self.audio_queue.get(timeout=1)
                    
                    # Transcribe the chunk and get words with timing
                    words_with_timing = self.transcribe_audio_chunk(frames)
                    
                    # Display words progressively
                    if words_with_timing:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"\n[{timestamp}] ", end="", flush=True)
                        
                        # Check if we have actual word-level data
                        has_word_timing = any('word' in word_info and len(word_info['word'].strip()) > 0 for word_info in words_with_timing)
                        
                        if has_word_timing:
                            # Display with word-level timing and confidence
                            for word_info in words_with_timing:
                                word = word_info['word'].strip()
                                if not word:
                                    continue
                                    
                                confidence = word_info.get('probability', 1.0)
                                
                                # Color coding based on confidence (if terminal supports it)
                                if confidence > 0.8:
                                    color_code = "\033[92m"  # Green for high confidence
                                elif confidence > 0.6:
                                    color_code = "\033[93m"  # Yellow for medium confidence
                                else:
                                    color_code = "\033[91m"  # Red for low confidence
                                
                                reset_code = "\033[0m"
                                
                                # Print word with timing and confidence
                                print(f"{color_code}{word}{reset_code}", end=" ", flush=True)
                                
                                # Add a small delay to simulate real-time word appearance
                                time.sleep(0.1)
                        else:
                            # Fallback: simple word-by-word display
                            full_text = " ".join([w.get('word', '') for w in words_with_timing]).strip()
                            if full_text:
                                words = full_text.split()
                                for word in words:
                                    print(f"{word}", end=" ", flush=True)
                                    time.sleep(0.15)
                        
                        print()  # New line after all words in this chunk
                    
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_transcription()
    
    def stop_transcription(self):
        """Stop transcription and cleanup"""
        print("\n🛑 Stopping transcription...")
        self.is_recording = False
        self.audio.terminate()
        print("✅ Transcription stopped.")

def main():
    # Initialize transcriber
    # You can adjust these parameters:
    # - model_size: "tiny", "base", "small", "medium", "large-v2", "large-v3"
    # - device: "cuda" for GPU, "cpu" for CPU
    # - compute_type: "float16", "int8" (for GPU), "int8" (for CPU)
    
    transcriber = RealTimeTranscriber(
        model_size="base",  # Using base model for faster real-time processing
        device="cpu",       # Using CPU to avoid CUDA/cuDNN issues
        compute_type="int8" # INT8 for CPU optimization
    )
    
    try:
        transcriber.start_transcription()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have a microphone connected and pyaudio installed.")
        print("Install pyaudio with: pip install pyaudio")

if __name__ == "__main__":
    main()