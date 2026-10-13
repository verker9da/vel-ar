"""
Dual-Language Text-to-Speech Generator for Arabic Learning
Uses Edge TTS for high-quality English and Arabic voices
"""

import os
import asyncio
import subprocess
from pathlib import Path
import edge_tts

# Voice configurations
ENGLISH_VOICE = "en-US-GuyNeural"  # Male English voice
ARABIC_VOICE = "ar-SA-HamedNeural"  # Male Arabic voice (Saudi Arabia)

# Alternative Arabic voices:
# ar-SA-ZariyahNeural (Female, Saudi Arabia)
# ar-EG-SalmaNeural (Female, Egypt)
# ar-EG-ShakirNeural (Male, Egypt)
# ar-AE-FatimaNeural (Female, UAE)
# ar-AE-HamdanNeural (Male, UAE)


def configure_edge_tts():
    """Ensure edge_tts connects to Microsoft's active endpoint to avoid 403 on cloud runners."""
    try:
        import edge_tts.constants
        import edge_tts.communicate
        token = getattr(edge_tts.constants, "TRUSTED_CLIENT_TOKEN", "6A5AA1D4EAFF4E9FB37E23D68491D6F4")
        new_url = (
            "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
            f"?Ocp-Apim-Subscription-Key={token}"
        )
        edge_tts.constants.WSS_URL = new_url
        edge_tts.communicate.WSS_URL = new_url
    except Exception:
        pass


async def generate_single_audio(text: str, voice: str, output_path: str):
    """Generate audio for a single text using specified voice with active endpoint and retry"""
    configure_edge_tts()
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            out = Path(output_path)
            if out.exists() and out.stat().st_size > 200:
                return
        except Exception as e:
            print(f"  TTS attempt {attempt + 1} error: {e}")
            await asyncio.sleep(1)

    try:
        from gtts import gTTS
        lang = "ar" if "ar" in voice.lower() else "en"
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
    except Exception:
        pass


def get_audio_duration(audio_file: str) -> float:
    """Get audio duration in seconds using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 2.0


def generate_phrase_audio(phrase_data: dict, output_dir: str, phrase_index: int):
    """
    Generate audio for a single phrase with English and Arabic

    Creates:
    - english_X.mp3: English phrase
    - arabic_X.mp3: Arabic translation
    - combined_X.mp3: English -> pause -> Arabic -> pause
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    english_text = phrase_data["english"]
    arabic_text = phrase_data["arabic"]

    english_file = output_dir / f"english_{phrase_index}.mp3"
    arabic_file = output_dir / f"arabic_{phrase_index}.mp3"
    combined_file = output_dir / f"combined_{phrase_index}.mp3"
    pause_file = output_dir / f"pause_{phrase_index}.mp3"

    print(f"[tts] Generating audio for phrase {phrase_index}...")

    # Generate English audio
    asyncio.run(generate_single_audio(english_text, ENGLISH_VOICE, str(english_file)))
    print(f"[tts]   ✅ English: {english_text[:50]}...")

    # Generate Arabic audio
    asyncio.run(generate_single_audio(arabic_text, ARABIC_VOICE, str(arabic_file)))
    print(f"[tts]   ✅ Arabic: {arabic_text[:30]}...")

    # Get durations
    en_duration = get_audio_duration(str(english_file))
    ar_duration = get_audio_duration(str(arabic_file))
    
    # Create pause audio (1000ms silence) - use same format as input
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "1.0", "-c:a", "libmp3lame", "-q:a", "2", str(pause_file)
    ]
    subprocess.run(cmd, capture_output=True)
    
    # Combine using concat demuxer with proper path escaping
    concat_list = output_dir / f"concat_{phrase_index}.txt"
    
    # Write file list with proper escaping for Windows paths
    files_to_concat = [english_file, pause_file, arabic_file, pause_file]
    with open(concat_list, "w", encoding="utf-8") as f:
        for fpath in files_to_concat:
            # Get absolute path and escape for ffmpeg
            abs_path = str(fpath.resolve())
            # Escape single quotes and backslashes for ffmpeg concat demuxer
            abs_path = abs_path.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{abs_path}'\n")
    
    # Combine files using copy codec (no re-encoding)
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(combined_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # If concat demuxer fails, try alternative approach
    if result.returncode != 0 or not combined_file.exists() or combined_file.stat().st_size == 0:
        print(f"[tts]   Warning: Concat demuxer failed, trying filter_complex...")
        
        # Use filter_complex with proper format
        cmd = [
            "ffmpeg", "-y",
            "-i", str(english_file),
            "-i", str(pause_file),
            "-i", str(arabic_file),
            "-i", str(pause_file),
            "-filter_complex", "[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[out]",
            "-map", "[out]", "-c:a", "libmp3lame", "-q:a", "2", str(combined_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[tts]   Error: Both methods failed!")
            print(f"[tts]   stderr: {result.stderr[:200]}")
    
    # Cleanup temp files
    if pause_file.exists():
        pause_file.unlink()
    if concat_list.exists():
        concat_list.unlink()
    
    # Calculate total duration
    if combined_file.exists() and combined_file.stat().st_size > 0:
        total_duration = get_audio_duration(str(combined_file))
        print(f"[tts]   ✅ Combined audio saved ({total_duration:.2f}s)")
    else:
        total_duration = en_duration + 1.0 + ar_duration + 1.0
        print(f"[tts]   ❌ Combined audio failed ({total_duration:.2f}s estimated)")
    
    return {
        "english": str(english_file),
        "arabic": str(arabic_file),
        "combined": str(combined_file),
        "duration": total_duration
    }


def generate_all_audio(phrases: list, output_dir: str = "audio"):
    """
    Generate audio for all phrases

    Returns list of audio info dicts
    """

    audio_files = []

    for i, phrase in enumerate(phrases):
        audio_info = generate_phrase_audio(phrase, output_dir, i)
        audio_files.append(audio_info)

    print(f"\n[tts] ✅ Generated audio for {len(phrases)} phrases")

    # Calculate total duration
    total_duration = sum(info["duration"] for info in audio_files)
    print(f"[tts] Total duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")

    return audio_files


def create_final_narration(audio_files: list, output_file: str):
    """
    Combine all phrase audio into final narration
    Uses filter_complex for maximum compatibility
    """

    print("[tts] Creating final narration...")

    # Get list of valid audio files
    input_files = []
    for audio_info in audio_files:
        combined_path = Path(audio_info["combined"])
        if combined_path.exists():
            input_files.append(str(combined_path.resolve()))
            print(f"[tts]   Adding: {combined_path}")
        else:
            print(f"[tts]   Warning: File not found: {combined_path}")

    if not input_files:
        print("[tts] ❌ No valid audio files to combine!")
        return None

    # Method 1: Try concat demuxer first (fastest - no re-encoding)
    concat_file = Path(output_file).parent / "narration_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for audio_path in input_files:
            # Escape single quotes for ffmpeg concat demuxer
            path_str = audio_path.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{path_str}'\n")

    print(f"[tts] Concat file created: {concat_file} ({concat_file.stat().st_size} bytes)")

    # Try concat demuxer with copy codec
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy",
        str(output_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Cleanup concat file
    if concat_file.exists():
        concat_file.unlink()

    # Check if successful
    if result.returncode == 0 and Path(output_file).exists() and Path(output_file).stat().st_size > 0:
        duration = get_audio_duration(str(output_file))
        print(f"[tts] ✅ Final narration saved: {output_file}")
        print(f"[tts] Duration: {duration:.1f} seconds")
        return output_file

    # Method 2: If concat demuxer fails, use filter_complex
    print(f"[tts] ⚠️ Concat demuxer failed, using filter_complex method...")

    # Build filter_complex for concatenation
    num_files = len(input_files)
    filter_parts = []
    concat_inputs = ""

    for i in range(num_files):
        concat_inputs += f"[{i}:a]"

    filter_complex = f"{concat_inputs}concat=n={num_files}:v=0:a=1[out]"

    # Build ffmpeg command with multiple inputs
    cmd = ["ffmpeg", "-y"]
    for audio_path in input_files:
        cmd.extend(["-i", audio_path])

    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "aac", "-b:a", "192k",
        str(output_file)
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0 and Path(output_file).exists() and Path(output_file).stat().st_size > 0:
        duration = get_audio_duration(str(output_file))
        print(f"[tts] ✅ Final narration saved: {output_file}")
        print(f"[tts] Duration: {duration:.1f} seconds")
        return output_file
    else:
        print(f"[tts] ❌ Failed to create final narration")
        if result.stderr:
            print(f"[tts] Error: {result.stderr[:500]}")
        return None


if __name__ == "__main__":
    # Test TTS generation
    test_phrases = [
        {
            "english": "Good morning! How are you?",
            "arabic": "صباح الخير! كيف حالك؟",
            "pronunciation": "Sabaah al-khayr! Kayfa haaluk?"
        },
        {
            "english": "Thank you very much!",
            "arabic": "شكراً جزيلاً!",
            "pronunciation": "Shukran jazeelan!"
        },
        {
            "english": "Where is the bathroom?",
            "arabic": "أين الحمام؟",
            "pronunciation": "Ayna al-hammaam?"
        }
    ]

    # Generate audio for all phrases
    audio_files = generate_all_audio(test_phrases, "test_output/audio")

    # Create final narration
    create_final_narration(audio_files, "test_output/final_narration.mp3")

    print("\n✅ Test audio generation complete!")
