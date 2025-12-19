import asyncio
import logging
import os
import edge_tts

logger = logging.getLogger(__name__)

# Voice Options (Indian Female voices for smooth interaction)
# en-IN-NeerjaNeural (Indian Female, Professional and Clear)
# en-IN-NeerjaExpressiveNeural (Indian Female, More Expressive)
# Alternative US voices:
# en-US-AriaNeural (Female, Professional)
# en-US-JennyNeural (Female, Friendly and Natural)
# en-US-SaraNeural (Female, Conversational)
DEFAULT_VOICE = "en-US-JennyNeural"  # US female voice (very smooth, friendly & natural) for interviews

async def generate_audio_edge(text, output_path, voice=DEFAULT_VOICE):
    """
    Generates audio using edge-tts library and saves to file.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
        # Verify file was created and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"Edge TTS Audio generated at {output_path}")
            return True
        else:
            logger.error("Edge TTS: Audio file not created or empty")
            return False
    except Exception as e:
        logger.error(f"Edge TTS Generation Error: {e}")
        return False

def generate_audio_sync(text, output_path, voice=DEFAULT_VOICE):
    """
    Synchronous wrapper for generate_audio_edge (File-based) with fallback to gTTS.
    """
    try:
        # Try Edge TTS first
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_audio_edge(text, output_path, voice))
        loop.close()
        
        if result:
            return True
        else:
            # Fallback to gTTS
            logger.warning("Edge TTS failed, falling back to gTTS")
            return generate_audio_gtts(text, output_path)
            
    except Exception as e:
        logger.error(f"Sync Edge TTS Error: {e}")
        # Fallback to gTTS
        logger.warning("Edge TTS error, falling back to gTTS")
        try:
            return generate_audio_gtts(text, output_path)
        except Exception as gtts_error:
            logger.error(f"gTTS fallback also failed: {gtts_error}")
            return False

def generate_audio_gtts(text, output_path):
    """
    Fallback TTS using Google Text-to-Speech (gTTS).
    """
    try:
        from gtts import gTTS
        
        logger.info(f"Generating audio with gTTS (Indian accent): {output_path}")
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        tts.save(output_path)
        
        # Verify file was created
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"gTTS Audio generated at {output_path}")
            return True
        else:
            logger.error("gTTS: Audio file not created or empty")
            return False
            
    except ImportError:
        logger.error("gTTS not installed. Install with: pip install gtts")
        return False
    except Exception as e:
        logger.error(f"gTTS Generation Error: {e}")
        return False

async def generate_audio_memory_edge(text, voice=DEFAULT_VOICE):
    """
    Generates audio bytes in-memory using edge-tts.
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        if len(audio_data) > 0:
            return audio_data
        else:
            logger.error("Edge TTS: No audio data received")
            return None
    except Exception as e:
        logger.error(f"Edge TTS Memory Error: {e}")
        return None

def generate_audio_memory_sync(text, voice=DEFAULT_VOICE):
    """
    Synchronous wrapper for in-memory generation with fallback to gTTS.
    """
    try:
        # Try Edge TTS first
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_audio_memory_edge(text, voice))
        loop.close()
        
        if result and len(result) > 0:
            return result
        else:
            # Fallback to gTTS in memory
            logger.warning("Edge TTS memory generation failed, falling back to gTTS")
            return generate_audio_gtts_memory(text)
            
    except Exception as e:
        logger.error(f"Sync Edge TTS Memory Error: {e}")
        # Fallback to gTTS
        logger.warning("Edge TTS error, falling back to gTTS memory")
        try:
            return generate_audio_gtts_memory(text)
        except Exception as gtts_error:
            logger.error(f"gTTS memory fallback also failed: {gtts_error}")
            return None

def generate_audio_gtts_memory(text):
    """
    Fallback TTS using gTTS for in-memory generation.
    """
    try:
        from gtts import gTTS
        import io
        
        logger.info("Generating audio with gTTS (Indian accent, in-memory)")
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        
        # Save to BytesIO buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_data = audio_buffer.read()
        
        if len(audio_data) > 0:
            logger.info(f"gTTS audio generated in memory ({len(audio_data)} bytes)")
            return audio_data
        else:
            logger.error("gTTS: No audio data generated")
            return None
            
    except ImportError:
        logger.error("gTTS not installed. Install with: pip install gtts")
        return None
    except Exception as e:
        logger.error(f"gTTS Memory Generation Error: {e}")
        return None
