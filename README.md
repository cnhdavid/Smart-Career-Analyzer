# 🎯 Smart Career & Skill-Gap Analyzer

An AI-powered web application that analyzes resumes to provide career readiness insights, skill gap analysis, and personalized learning recommendations.

![Tech Stack](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3-cyan)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

## ✨ Features

- 📄 **PDF Resume Upload** - Drag & drop interface with real-time processing
- 🤖 **AI-Powered Analysis** - Uses LangChain with OpenAI/Mock mode for skill extraction
- 📊 **Interactive Visualizations** - Radar charts comparing skills to industry standards
- 🎯 **Role Matching** - Match percentage for Data Scientist, AI Engineer, and Full-Stack Developer roles
- 🚀 **Learning Roadmap** - Personalized recommendations with resources and timelines
- 🌓 **Dark Mode Support** - Beautiful, responsive UI with dark/light themes
- 🔄 **Mock Mode** - Fully functional demo without API keys

## 🏗️ Project Structure

```
Smart Portfolio Analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── pdf_parser.py       # PDF text extraction (PyMuPDF)
│   │   └── ai_analyzer.py      # AI analysis with LangChain
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx
    │   │   ├── UploadZone.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── RadarChart.jsx
    │   │   ├── RoleMatchCard.jsx
    │   │   ├── SkillsList.jsx
    │   │   └── Roadmap.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    └── tailwind.config.js
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 16+**
- **npm or yarn**

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Configure OpenAI API:
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

6. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 🎮 Usage

1. **Upload Resume**: Drag and drop a PDF resume or click to browse
2. **Processing**: Watch the AI analyze your skills and experience
3. **View Results**: 
   - See your skill radar chart
   - Check role match percentages
   - Review skill gaps for each role
   - Get personalized learning recommendations

## 🔧 API Endpoints

### `POST /api/analyze-resume`
Upload and analyze a PDF resume.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response:**
```json
{
  "skills": ["Python", "JavaScript", "React", ...],
  "experience_years": 3.5,
  "role_matches": {
    "Data Scientist": 75.0,
    "AI Engineer": 60.0,
    "Full-Stack Developer": 80.0
  },
  "skill_gaps": {
    "Data Scientist": ["R", "Statistics", ...],
    ...
  },
  "radar_data": {
    "labels": ["Programming", "ML/AI", ...],
    "datasets": [...]
  },
  "recommendations": [
    {
      "skill": "Machine Learning",
      "priority": "High",
      "resource": "Coursera - ML Specialization",
      "timeframe": "3-4 months"
    },
    ...
  ]
}
```

### `GET /api/health`
Check API health and mode (mock/live).

## 🎨 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **PyMuPDF (fitz)** - PDF parsing
- **LangChain** - AI orchestration
- **OpenAI** - Language model (optional)
- **Python-dotenv** - Environment management

## 🧪 Mock Mode

The application includes a fully functional mock mode that works without an OpenAI API key. It uses intelligent pattern matching and heuristics to:

- Extract skills from resume text
- Estimate years of experience
- Calculate role match percentages
- Generate skill gap reports
- Provide learning recommendations

This makes the app perfect for portfolio demonstrations!

## 🌟 Key Features Explained

### AI Analysis
- Extracts technical skills using pattern matching or LLM
- Compares against 3 standard role profiles
- Generates match scores based on skill overlap
- Identifies top skill gaps per role

### Radar Chart
- Visual comparison of your skills vs industry standards
- 5 categories: Programming, ML/AI, Frontend, Backend, DevOps
- Interactive tooltips and legends

### Learning Roadmap
- Prioritized skill recommendations (High/Medium/Low)
- Curated learning resources
- Estimated time commitments
- Skill development tracking

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here  # Optional - app works in mock mode without it
```

## 🔒 Security Notes

- Never commit `.env` files
- API keys should be kept secure
- CORS is configured for local development only
- Adjust CORS settings for production deployment

## 🚢 Deployment

### Backend (Render/Railway/Heroku)
1. Set environment variables in platform dashboard
2. Use `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Update CORS origins to include frontend URL

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Update API_URL in UploadZone.jsx to backend URL
3. Deploy `dist` folder

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

## 📄 License

MIT License - feel free to use for your own portfolio

## 👨‍💻 Author

Built as a portfolio demonstration of full-stack AI engineering skills.

---

**Note**: This project demonstrates proficiency in:
- Full-stack development (React + FastAPI)
- AI/ML integration (LangChain, OpenAI)
- Modern UI/UX (Tailwind, Recharts)
- PDF processing and data extraction
- RESTful API design
- Responsive design and dark mode
