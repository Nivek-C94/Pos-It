# Pos-It

Pos-It is a GUI automation tool that enhances ChatGPT's abilities by combining:

- 🤖 ChatGPT API for intelligent product data generation
- 📸 Reverse image search for product recognition
- 🌐 Botasaurus driver for web automation
- 🛍 Posting to eBay, Mercari, Facebook

## Features
- Upload product images
- Automatically identify and describe items
- Auto-generate pricing and listing details
- Post listings on major marketplaces

## Usage (Planned)
1. Start the GUI
2. Upload one or more images
3. Confirm or adjust suggested details
4. Click "Post" to publish to selected platforms

## Structure (MVP)
```
pos-it/
├── gui/                  # GUI app (PyQt5 or Tkinter)
├── services/             # ChatGPT + reverse search logic
├── platforms/            # eBay / Mercari / Facebook automation
├── automation/           # Driver pool management
├── models/               # Request/response/data models
├── utils/                # Logging, settings, helpers
└── main.py               # Entrypoint
```