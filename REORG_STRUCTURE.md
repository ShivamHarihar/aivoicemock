/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── app.py
│   ├── src/
│   │   ├── __init__.py
│   │   ├── audio_analyzer.py
│   │   ├── coqui_tts.py
│   │   ├── edge_tts_client.py
│   │   ├── grok_client.py
│   │   ├── groq_client.py
│   │   ├── interview_engine.py
│   │   ├── list_models.py
│   │   ├── memory_store.py
│   │   ├── mistake_detector.py
│   │   ├── pdf_generator.py
│   │   ├── prompts.py
│   │   ├── question_packs.py
│   │   ├── resume_analyzer.py
│   │   ├── resume_recreator.py
│   │   ├── scoring.py
│   │   ├── spacy_parser.py
│   │   ├── translator.py
│   │   ├── utils.py
│   │   ├── voice_modulator.py
│   │   └── whisper_stt.py
│   └── tests/
├── frontend/
│   ├── public/          (formerly backend/static)
│   │   ├── audio/
│   │   ├── images/
│   │   ├── uploads/
│   │   ├── css/
│   │   └── js/
│   └── src/             (formerly backend/templates)
│       ├── index.html
│       ├── dashboard.html
│       └── ... (other templates)
├── models/              (metadata only)
├── scripts/
│   └── verify_system.py
├── configs/
│   └── requirements.txt
├── docs/
├── .vscode/
├── .env
├── .gitignore
├── README.md
└── REORG_STRUCTURE.md
