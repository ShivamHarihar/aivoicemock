let mediaRecorder;
let audioChunks = [];
let sessionId = null;

// VAD Configuration
const VAD_THRESHOLD = 0.01;
const SILENCE_DURATION = 1500; // 1.5 seconds of silence before processing (reduced for faster response)
const SPEECH_END_BUFFER = 800; // Additional buffer after silence detected

let audioContext;
let analyser;
let microphone;
let silenceStart = Date.now();
let isSpeaking = false;
let vadInterval;
let isProcessing = false; // Prevent overlapping processing

// Timer and summary trigger
let interviewStartTime = null;
let summaryTriggered = false;
const QA_PHASE_DURATION = 2 * 60 * 1000; // 2 minutes in milliseconds

async function startInterview() {
    const mode = document.getElementById('mode').value;
    const jobRole = document.getElementById('jobRole') ? document.getElementById('jobRole').value : '';
    const company = document.getElementById('company') ? document.getElementById('company').value : '';
    const resumeFile = document.getElementById('resume').files[0];

    let resumeText = '';

    // Extract text from resume file if provided
    if (resumeFile) {
        try {
            if (resumeFile.name.endsWith('.txt')) {
                // Read text file
                resumeText = await resumeFile.text();
            } else if (resumeFile.name.endsWith('.pdf')) {
                // For PDF, we'll upload it and let backend handle parsing
                const formData = new FormData();
                formData.append('resume', resumeFile);
                const uploadResponse = await fetch('/upload_profile', { method: 'POST', body: formData });
                const uploadData = await uploadResponse.json();
                // The upload_profile endpoint returns parsed text
                resumeText = uploadData.text_content || '';
            }
        } catch (error) {
            console.error('Error reading resume file:', error);
            // Continue without resume text
        }
    }

    const response = await fetch('/start_call_interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            mode: mode,
            job_role: jobRole,
            company: company,
            resume_text: resumeText  // Send resume text to backend
        })
    });

    const data = await response.json();
    if (data.session_id) {
        sessionId = data.session_id;
        const audioUrl = encodeURIComponent(data.audio_url);
        const message = encodeURIComponent(data.message);
        window.location.href = `/interview?session_id=${sessionId}&audio=${audioUrl}&text=${message}`;
    }
}

// Interview Page Initialization
if (window.location.pathname === '/interview') {
    const urlParams = new URLSearchParams(window.location.search);
    sessionId = urlParams.get('session_id');
    const greetingAudio = urlParams.get('audio');
    const greetingText = urlParams.get('text');

    const controls = document.querySelector('.controls');
    if (controls) controls.style.display = 'none';

    const statusEl = document.getElementById('status');
    if (statusEl) statusEl.innerText = "AI is greeting you...";

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            initVAD(stream);

            // Play greeting first, then start listening
            if (greetingAudio && greetingText) {
                const decodedAudio = decodeURIComponent(greetingAudio);
                const decodedText = decodeURIComponent(greetingText);

                // Play greeting audio immediately
                playGreeting(decodedAudio, decodedText);
            } else {
                // No greeting, start listening immediately
                startRecording();
            }
        })
        .catch(err => {
            console.error("Error accessing microphone:", err);
            alert("Microphone access is required for this interview.");
        });
}

function playGreeting(audioUrl, text) {
    const statusEl = document.getElementById('status');
    statusEl.innerText = "AI: " + text;

    const circles = document.querySelectorAll('.visualizer-circle');
    circles.forEach(c => c.style.animation = 'pulse 1.5s infinite');

    // Play the greeting audio
    const audio = new Audio(audioUrl);
    audio.play()
        .then(() => {
            audio.onended = () => {
                statusEl.innerText = "Listening...";
                circles.forEach(c => c.style.animation = 'none');
                // Start interview timer
                interviewStartTime = Date.now();
                startSummaryCheck();
                // Start listening after greeting finishes
                startRecording();
            };
        })
        .catch(err => {
            console.error("Greeting audio failed:", err);
            // If audio fails, still start listening
            statusEl.innerText = "Listening...";
            circles.forEach(c => c.style.animation = 'none');
            // Start interview timer
            interviewStartTime = Date.now();
            startSummaryCheck();
            startRecording();
        });
}

// Check for summary phase every second and update timer display
function startSummaryCheck() {
    // Show timer container
    const timerContainer = document.getElementById('timer-container');
    if (timerContainer) {
        timerContainer.style.display = 'block';
    }

    setInterval(() => {
        if (!interviewStartTime) return;

        const elapsed = Date.now() - interviewStartTime;
        const elapsedSeconds = Math.floor(elapsed / 1000);
        const TOTAL_DURATION = 4 * 60; // 4 minutes in seconds
        const QA_PHASE_SECONDS = 2 * 60; // 2 minutes in seconds

        // Update timer display
        updateTimerDisplay(elapsedSeconds, TOTAL_DURATION, QA_PHASE_SECONDS);

        // Trigger summary at 2 minutes
        if (!summaryTriggered && elapsed >= QA_PHASE_DURATION) {
            summaryTriggered = true;
            console.log('2 minutes elapsed - triggering summary');
            triggerSummary();
        }
    }, 1000); // Check every second
}

// Update timer display
function updateTimerDisplay(elapsedSeconds, totalDuration, qaPhaseSeconds) {
    const remaining = Math.max(0, totalDuration - elapsedSeconds);

    // Determine phase
    let phase = 'Q&A Phase';
    let phaseClass = 'qa-phase';
    let phaseRemaining = remaining;

    if (elapsedSeconds >= qaPhaseSeconds) {
        phase = 'Summary Phase';
        phaseClass = 'summary-phase';
        phaseRemaining = Math.max(0, totalDuration - elapsedSeconds);
    } else {
        phaseRemaining = Math.max(0, qaPhaseSeconds - elapsedSeconds);
    }

    // Update phase display
    const phaseEl = document.getElementById('timer-phase');
    if (phaseEl) {
        phaseEl.textContent = phase;
        phaseEl.className = `timer-phase ${phaseClass}`;
    }

    // Format time as MM:SS
    const minutes = Math.floor(phaseRemaining / 60);
    const seconds = phaseRemaining % 60;
    const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;

    // Update time display
    const timeEl = document.getElementById('timer-time');
    if (timeEl) {
        timeEl.textContent = timeString;

        // Add warning/critical classes
        timeEl.classList.remove('warning', 'critical');
        if (phaseRemaining <= 30) {
            timeEl.classList.add('critical');
        } else if (phaseRemaining <= 60) {
            timeEl.classList.add('warning');
        }
    }

    // Update progress bar
    const progressEl = document.getElementById('timer-progress');
    if (progressEl) {
        let progress;
        if (elapsedSeconds < qaPhaseSeconds) {
            // Q&A phase progress
            progress = (elapsedSeconds / qaPhaseSeconds) * 100;
        } else {
            // Summary phase progress
            const summaryElapsed = elapsedSeconds - qaPhaseSeconds;
            const summaryDuration = totalDuration - qaPhaseSeconds;
            progress = (summaryElapsed / summaryDuration) * 100;
        }
        progressEl.style.width = `${Math.min(100, progress)}%`;
    }
}

// Trigger the summary phase
function triggerSummary() {
    // Stop listening
    if (recognition) {
        try {
            recognition.stop();
        } catch (e) {
            console.log('Recognition already stopped');
        }
    }

    isProcessing = true;
    const statusEl = document.getElementById('status');
    if (statusEl) {
        statusEl.innerText = "Generating performance summary...";
    }

    // Send trigger to backend
    console.log('Requesting performance summary from backend');
    fetch('/process_voice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            user_text: "[AUTO_SUMMARY_TRIGGER]"
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log('Summary received:', data);

            if (data.error) {
                console.error('Backend error:', data.error);
                if (statusEl) {
                    statusEl.innerText = "Error: " + data.error;
                }
                return;
            }

            if (data.full_text) {
                console.log('Playing summary');
                playResponse(data.audio_base64, data.full_text, true);
            } else {
                console.error('No summary text received');
                if (statusEl) {
                    statusEl.innerText = "Error: No summary generated";
                }
            }
        })
        .catch(err => {
            console.error('Error getting summary:', err);
            if (statusEl) {
                statusEl.innerText = "Error generating summary";
            }
        });
}

// Browser STT Configuration
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let recognitionTimeout;
let lastTranscript = '';
let speechEndTimer;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true; // Changed to true for better control
    recognition.lang = 'en-US';
    recognition.interimResults = true; // Enable interim results to track ongoing speech
    recognition.maxAlternatives = 1;
}

function initVAD(stream) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);
    analyser.fftSize = 2048;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    vadInterval = setInterval(() => {
        analyser.getByteTimeDomainData(dataArray);
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
            const x = (dataArray[i] - 128) / 128.0;
            sum += x * x;
        }
        const rms = Math.sqrt(sum / bufferLength);
        updateVisualizer(rms);
    }, 100);
}

function updateVisualizer(volume) {
    const circles = document.querySelectorAll('.visualizer-circle');
    if (volume > VAD_THRESHOLD) {
        circles.forEach((c, i) => {
            c.style.animation = `pulse ${1.5 - i * 0.2}s infinite`;
        });
    } else {
        circles.forEach(c => {
            c.style.animation = 'none';
        });
    }
}

let currentAudio = null;

function startRecording() {
    if (recognition && !isProcessing) {
        try {
            if (currentAudio) {
                currentAudio.pause();
                currentAudio = null;
                speechSynthesis.cancel();
                console.log("Barge-in: AI audio stopped.");
            }

            // Clear any existing timers
            if (speechEndTimer) {
                clearTimeout(speechEndTimer);
                speechEndTimer = null;
            }

            lastTranscript = '';
            recognition.start();
            document.getElementById('status').innerText = "Listening...";
            const micIcon = document.querySelector('.mic-icon');
            if (micIcon) micIcon.style.color = '#ef4444';

            recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }

                // Show what's being heard in real-time
                const instructionText = document.querySelector('.instruction-text');
                if (interimTranscript && instructionText) {
                    instructionText.innerText = `Hearing: "${interimTranscript}..."`;
                    instructionText.style.color = '#10b981';
                }

                // Update last transcript
                if (finalTranscript) {
                    lastTranscript = finalTranscript;
                    console.log("Final transcript:", finalTranscript);
                    if (instructionText) {
                        instructionText.innerText = `Got it: "${finalTranscript}" - Waiting for you to finish...`;
                        instructionText.style.color = '#3b82f6';
                    }
                } else if (interimTranscript) {
                    console.log("Interim transcript:", interimTranscript);
                }

                // Clear existing timer
                if (speechEndTimer) {
                    clearTimeout(speechEndTimer);
                }

                // Set new timer - only process after silence
                speechEndTimer = setTimeout(() => {
                    if (lastTranscript && lastTranscript.trim()) {
                        console.log("Speech ended, processing:", lastTranscript);
                        recognition.stop();
                        document.getElementById('status').innerText = "Processing...";
                        if (instructionText) {
                            instructionText.innerText = "Analyzing your answer...";
                            instructionText.style.color = '#f59e0b';
                        }
                        isProcessing = true;
                        sendText(lastTranscript);
                        lastTranscript = '';
                    }
                }, SILENCE_DURATION); // Wait 1.5 seconds of silence
            };

            recognition.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                if (event.error === 'no-speech') {
                    // Restart listening if no speech detected
                    setTimeout(() => {
                        if (!isProcessing) {
                            startRecording();
                        }
                    }, 500);
                } else if (event.error === 'aborted') {
                    // Normal stop, don't restart
                    console.log("Recognition aborted normally");
                } else {
                    // Other errors, try to restart
                    setTimeout(() => {
                        if (!isProcessing) {
                            startRecording();
                        }
                    }, 1000);
                }
            };

            recognition.onend = () => {
                console.log("Recognition ended");
                // Don't automatically restart if we're processing
                if (!isProcessing) {
                    setTimeout(startRecording, 300);
                }
            };

        } catch (e) {
            console.error("Recognition start failed", e);
            setTimeout(() => {
                if (!isProcessing) {
                    startRecording();
                }
            }, 1000);
        }
    }
}

function stopRecording() {
    // Clear any pending timers
    if (speechEndTimer) {
        clearTimeout(speechEndTimer);
        speechEndTimer = null;
    }

    // Stop recognition
    if (recognition) {
        try {
            recognition.stop();
        } catch (e) {
            console.log("Recognition already stopped");
        }
    }

    // Process any accumulated transcript
    if (lastTranscript && lastTranscript.trim()) {
        console.log("Force sending:", lastTranscript);
        document.getElementById('status').innerText = "Processing...";
        const micIcon = document.querySelector('.mic-icon');
        if (micIcon) micIcon.style.color = 'white';

        isProcessing = true;
        sendText(lastTranscript);
        lastTranscript = '';
    }
}

function sendText(text) {
    if (!text || !text.trim()) return;

    document.getElementById('status').innerText = "Processing...";
    console.log('Sending text:', text);

    fetch('/process_voice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            user_text: text
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log('Response:', data);

            if (data.real_time_feedback) {
                window.lastFeedback = data.real_time_feedback;
                console.log('Real-time feedback:', data.real_time_feedback);
            }

            // Check if this is a summary phase response
            const isSummary = data.phase === 'summary' || data.interview_complete === true;
            console.log('Is summary phase:', isSummary, 'Phase:', data.phase, 'Complete:', data.interview_complete);

            playResponse(data.audio_base64, data.full_text, isSummary);
        })
        .catch(err => {
            console.error('Error:', err);
            document.getElementById('status').innerText = "Error occurred";
        });
}

function playResponse(audioData, text, isSummary = false) {
    console.log('playResponse called:', { hasAudio: !!audioData, isSummary });

    // CRITICAL: Stop any existing audio first to prevent double voice
    if (currentAudio) {
        try {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            currentAudio = null;
        } catch (e) {
            console.log('Error stopping previous audio:', e);
        }
    }

    // Also cancel any browser TTS that might be playing
    if (window.speechSynthesis) {
        speechSynthesis.cancel();
    }

    const statusEl = document.getElementById('status');

    if (isSummary) {
        statusEl.innerText = "AI is giving performance summary...";
    } else {
        statusEl.innerText = "Interviewer Speaking...";
    }

    const circles = document.querySelectorAll('.visualizer-circle');
    circles.forEach(c => c.style.animation = 'pulse 1.5s infinite');

    const onPlaybackComplete = () => {
        circles.forEach(c => c.style.animation = 'none');
        currentAudio = null;

        if (isSummary) {
            // Summary complete - redirect to results
            statusEl.innerText = "Interview Complete!";
            console.log('Summary complete - redirecting to results');
            setTimeout(() => {
                window.location.href = `/result?session_id=${sessionId}`;
            }, 2000);
        } else {
            // Normal Q&A - restart listening
            statusEl.innerText = "Listening...";
            // Add delay before starting to listen again
            setTimeout(() => {
                isProcessing = false; // Reset processing flag
                startRecording();
            }, 500); // 500ms delay after AI finishes speaking
        }
    };

    // Only play Edge TTS audio (no browser TTS fallback)
    if (audioData) {
        console.log('Playing audio...');
        const audioSrc = "data:audio/mp3;base64," + audioData;
        currentAudio = new Audio(audioSrc);
        currentAudio.play()
            .then(() => {
                currentAudio.onended = onPlaybackComplete;
            })
            .catch(e => {
                console.error("Audio play failed:", e);
                // If audio fails, just continue without speaking
                onPlaybackComplete();
            });
    } else {
        // No audio available, just continue
        console.log("No audio data - completing immediately");
        onPlaybackComplete();
    }
}

function resetSession() {
    isSpeaking = false;
    audioChunks = [];
    document.getElementById('status').innerText = "Your turn...";
    const controlsEl = document.querySelector('.controls');
    if (controlsEl) controlsEl.style.display = 'flex';

    speechSynthesis.cancel();
    console.log("Session reset manually.");
}

function endInterview() {
    fetch('/final_results', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
    })
        .then(res => res.json())
        .then(data => {
            window.location.href = `/result?session_id=${sessionId}`;
        });
}
