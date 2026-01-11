import { useState, useRef } from 'react'
import { Upload, FileText, AlertCircle, Loader2, Target, Sparkles, Lightbulb, BarChart3, Rocket } from 'lucide-react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const SAMPLE_RESUME = `John Doe
Software Engineer | 5 years of experience

TECHNICAL SKILLS:
- Programming Languages: Python, JavaScript, TypeScript, Java
- Web Technologies: React, Node.js, HTML, CSS, REST APIs
- Databases: PostgreSQL, MongoDB, Redis
- Tools & Platforms: Git, Docker, AWS, CI/CD
- Data Science: Pandas, NumPy, Scikit-learn, Data Visualization

PROFESSIONAL EXPERIENCE:
Senior Software Engineer at Tech Corp (2021-Present)
- Built scalable web applications using React and Node.js
- Implemented CI/CD pipelines with GitHub Actions
- Managed cloud infrastructure on AWS (EC2, S3, Lambda)
- Collaborated with data science team on ML model deployment

Software Developer at StartupXYZ (2019-2021)
- Developed full-stack applications with Python Django and React
- Designed and optimized PostgreSQL databases
- Implemented RESTful APIs serving 100K+ daily requests

EDUCATION:
Bachelor of Science in Computer Science
University of Technology (2015-2019)

CERTIFICATIONS:
- AWS Certified Solutions Architect
- MongoDB Certified Developer`

const POPULAR_ROLES = [
  // Technology
  'Data Scientist',
  'AI Engineer',
  'Full-Stack Developer',
  'Cloud Architect',
  'DevOps Engineer',
  'Software Architect',
  // Business & Management
  'Project Manager',
  'Product Manager',
  'Business Analyst',
  'Operations Manager',
  'Strategy Consultant',
  // Marketing & Sales
  'Marketing Manager',
  'Digital Marketing Director',
  'Sales Manager',
  'Business Development Manager',
  'Brand Manager',
  // Finance & Accounting
  'Financial Analyst',
  'Investment Analyst',
  'Finance Manager',
  'Controller',
  'Accountant',
  // Healthcare
  'Healthcare Administrator',
  'Clinical Manager',
  'Medical Director',
  'Healthcare Consultant',
  // Human Resources
  'HR Manager',
  'Talent Acquisition Lead',
  'People Operations Director',
  'HR Business Partner',
  // Design & Creative
  'UX Designer',
  'Creative Director',
  'Product Designer',
  'Brand Designer'
]

function UploadZone({ onAnalysisComplete, isLoading, setIsLoading }) {
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState(null)
  const [fileName, setFileName] = useState(null)
  const [targetRole, setTargetRole] = useState('')
  const [showRoleDropdown, setShowRoleDropdown] = useState(false)
  const [jobDescription, setJobDescription] = useState('')
  const fileInputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file) => {
    if (!file.name.endsWith('.pdf')) {
      setError('Please upload a PDF file')
      return
    }

    setError(null)
    setFileName(file.name)
    setIsLoading(true)

    const formData = new FormData()
    formData.append('file', file)
    if (targetRole) {
      formData.append('target_role', targetRole)
    }
    if (jobDescription) {
      formData.append('job_description', jobDescription)
    }

    try {
      const response = await axios.post(`${API_URL}/api/analyze-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onAnalysisComplete(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume. Please try again.')
      setIsLoading(false)
    }
  }

  const handleSampleResume = async () => {
    setError(null)
    setFileName('Sample Resume')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/analyze-text`, {
        text_resume: SAMPLE_RESUME,
        target_role: targetRole || null,
        job_description: jobDescription || null
      })

      onAnalysisComplete(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze sample resume. Please try again.')
      setIsLoading(false)
    }
  }

  const handleRoleSelect = (role) => {
    setTargetRole(role)
    setShowRoleDropdown(false)
  }

  const filteredRoles = POPULAR_ROLES.filter(role => 
    role.toLowerCase().includes(targetRole.toLowerCase())
  )

  const onButtonClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="max-w-3xl mx-auto mt-12">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
          Discover Your Career Potential
        </h2>
        <p className="text-lg text-gray-600 dark:text-gray-400">
          Upload your resume and get AI-powered insights on your skills and career readiness
        </p>
      </div>

      <div className="card mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Target className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold">Target Dream Job (Optional)</h3>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Specify your dream role to get personalized skill gap analysis
        </p>
        <div className="relative">
          <input
            type="text"
            value={targetRole}
            onChange={(e) => {
              setTargetRole(e.target.value)
              setShowRoleDropdown(true)
            }}
            onFocus={() => setShowRoleDropdown(true)}
            placeholder="e.g., Marketing Manager, Financial Analyst, Software Engineer..."
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            disabled={isLoading}
          />
          {showRoleDropdown && filteredRoles.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredRoles.map((role) => (
                <button
                  key={role}
                  onClick={() => handleRoleSelect(role)}
                  className="w-full text-left px-4 py-2 hover:bg-primary-50 dark:hover:bg-primary-900/20 text-gray-900 dark:text-gray-100 transition-colors"
                >
                  {role}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="card mb-6 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-200 dark:border-green-800">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-5 h-5 text-green-600" />
          <h3 className="text-lg font-semibold">Target Job Description (Optional)</h3>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 flex items-center gap-2">
          <Target className="w-4 h-4 text-green-600 flex-shrink-0" />
          <span><strong>Paste the Job Description here for a tailored analysis</strong> - Get precise match scores and ATS optimization tips</span>
        </p>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the full job description here...&#10;&#10;Example:&#10;Senior Software Engineer&#10;Requirements:&#10;- 5+ years of experience with Python and JavaScript&#10;- Strong knowledge of React, Node.js, and AWS&#10;- Experience with CI/CD pipelines..."
          className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 min-h-[120px] resize-y"
          disabled={isLoading}
        />
        <p className="text-xs text-gray-500 dark:text-gray-500 mt-2 flex items-start gap-2">
          <Lightbulb className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
          <span>When you provide a job description, the AI will act as a recruiter for that specific role and calculate your match score based on the exact requirements</span>
        </p>
      </div>

      <div
        className={`card relative ${
          dragActive ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : ''
        } ${isLoading ? 'opacity-75' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
          disabled={isLoading}
        />

        {isLoading ? (
          <div className="text-center py-16">
            <Loader2 className="w-16 h-16 mx-auto mb-4 text-primary-600 animate-spin" />
            <h3 className="text-xl font-semibold mb-2">Analyzing Your Resume</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Our AI is extracting skills and comparing them to industry standards...
            </p>
            {fileName && (
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                Processing: {fileName}
              </p>
            )}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="bg-primary-100 dark:bg-primary-900/30 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Upload className="w-10 h-10 text-primary-600 dark:text-primary-400" />
            </div>
            
            <h3 className="text-xl font-semibold mb-2">Upload Your Resume</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Drag and drop your PDF resume here, or click to browse
            </p>
            
            <div className="flex gap-3 justify-center">
              <button
                onClick={onButtonClick}
                className="btn-primary"
              >
                <FileText className="w-5 h-5 inline mr-2" />
                Choose File
              </button>
              
              <button
                onClick={handleSampleResume}
                className="btn-secondary flex items-center gap-2"
              >
                <Sparkles className="w-5 h-5" />
                Try Sample Resume
              </button>
            </div>
            
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-4">
              Supported format: PDF (Max 10MB) • Or try our sample resume
            </p>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <p className="text-red-800 dark:text-red-200">{error}</p>
          </div>
        )}
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <div className="bg-blue-100 dark:bg-blue-900/30 p-3 rounded-full">
              <Target className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <h4 className="font-semibold mb-1">Universal Role Matching</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            See how you match across ANY industry and role
          </p>
        </div>
        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <div className="bg-purple-100 dark:bg-purple-900/30 p-3 rounded-full">
              <BarChart3 className="w-8 h-8 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
          <h4 className="font-semibold mb-1">Competency Analysis</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Visual breakdown of your key competencies
          </p>
        </div>
        <div className="card text-center">
          <div className="flex justify-center mb-3">
            <div className="bg-green-100 dark:bg-green-900/30 p-3 rounded-full">
              <Rocket className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
          </div>
          <h4 className="font-semibold mb-1">Career Growth Path</h4>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Personalized recommendations for your next step
          </p>
        </div>
      </div>
    </div>
  )
}

export default UploadZone
