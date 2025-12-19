"""
Test script to verify Indian female voice generation using gTTS
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.src.edge_tts_client import generate_audio_sync

# Test text with Indian context
test_text = "Hello! I'm your AI interviewer. Welcome to your interview for the Data Analyst position at Amazon. I'm excited to learn more about you."
output_path = "test_indian_voice.mp3"

print("=" * 60)
print("Testing Indian Female Voice Generation")
print("=" * 60)
print(f"\nText: {test_text}")
print(f"Output: {output_path}\n")

# Generate audio
result = generate_audio_sync(test_text, output_path)

if result:
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"✅ SUCCESS: Indian accent audio generated!")
        print(f"   File: {output_path}")
        print(f"   Size: {size:,} bytes ({size/1024:.1f} KB)")
        print(f"\n🎧 You can play this file to hear the Indian female voice")
        print(f"   The voice should have an Indian accent")
        
        # Keep the file for manual testing
        print(f"\n📝 Note: File kept for your review. Delete manually when done.")
    else:
        print("❌ FAILED: Function returned True but file not found")
else:
    print("❌ FAILED: TTS generation failed")
    
print("=" * 60)
