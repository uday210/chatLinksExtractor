# 🔗 Chat Link Extractor

Extract, organize, and export links from chat histories (WhatsApp, Telegram, Discord, etc.) with intelligent grouping and deduplication.

## Features ✨

- **Multiple Input Methods**: Paste text directly or upload `.txt` files
- **Link Extraction**: Automatically finds HTTP, HTTPS, Telegram, YouTube, and custom links
- **Name Extraction**: Optional extraction of usernames and contact names
- **Month-wise Grouping**: Organize links by month and year from chat dates
- **Deduplication**: Remove duplicate links automatically
- **CSV Export**: Download results in CSV format for further analysis
- **Clean UI**: Built with Streamlit for a simple, intuitive interface

## Installation

### Local Development

1. **Clone the repository** (or initialize your project)
   ```bash
   git clone https://github.com/yourusername/chat-link-extractor.git
   cd chat-link-extractor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select Input Method**
   - Paste your chat history directly
   - Or upload a `.txt` file

2. **Configure Options**
   - Toggle "Include Names/Usernames" to extract contact names
   - Toggle "Group by Month" for temporal organization
   - Toggle "Remove Duplicates" for cleaner results

3. **Process**
   - Click "Extract & Process" button
   - View results in the table
   - Download as CSV

## Supported Chat Formats

- ✅ WhatsApp exports (`.txt`)
- ✅ Telegram exports (`.txt`)
- ✅ Discord exports (`.txt`)
- ✅ Any plain text with dates and links

### Example Format
```
12/25/2024, 10:30 - John: Check this out: https://example.com
12/25/2024, 10:35 - Sarah: I found this t.me/channel link
```

## Deployment to Railway

### Prerequisites
- GitHub account with the repository
- Railway.app account (free tier available)

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Chat Link Extractor"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Start New Project"
   - Select "Deploy from GitHub"
   - Connect your GitHub account and select this repository

3. **Configure Environment**
   - Railway auto-detects Python projects
   - It will install dependencies from `requirements.txt`

4. **Set Start Command**
   - In Railway settings, set the start command to:
   ```bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

5. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your app will be live at a Railway-provided URL

### Environment Variables (if needed)
None required for basic functionality. The app works out of the box.

## Project Structure

```
chat-link-extractor/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions for link extraction
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore file
```

## How It Works

### Link Extraction
The app uses regex patterns to find:
- Standard HTTP/HTTPS URLs
- Telegram links (`telegram.me/`, `t.me/`)
- YouTube links
- www links

### Date Parsing
Recognizes multiple date formats:
- `DD/MM/YYYY`, `MM/DD/YYYY`
- `DD-MM-YYYY`
- Named months: `12 Jan 2024`

### Name Extraction
Finds:
- @mentions (e.g., `@username`)
- Contact names at message start

### Month Grouping
Automatically groups extracted links by the month they were shared, making it easy to track link sharing patterns over time.

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, Regex
- **Deployment**: Railway
- **Language**: Python 3.8+

## Contributing

Feel free to fork, modify, and submit pull requests!

### Possible Enhancements
- [ ] Support for more chat platforms
- [ ] Advanced filtering options
- [ ] Link categorization by type
- [ ] Duplicate URL detection (by domain)
- [ ] Database integration for history
- [ ] URL validation and live checking

## License

MIT License - feel free to use this project for any purpose!

## Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation

---

**Made with ❤️ for chat history analysis**
