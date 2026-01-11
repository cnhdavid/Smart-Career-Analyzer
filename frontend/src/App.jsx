import { useState, useEffect } from 'react'
import { Moon, Sun } from 'lucide-react'
import UploadZone from './components/UploadZone'
import Dashboard from './components/Dashboard'
import Header from './components/Header'

function App() {
  const [darkMode, setDarkMode] = useState(true)
  const [analysisData, setAnalysisData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data)
    setIsLoading(false)
  }

  const handleReset = () => {
    setAnalysisData(null)
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <Header darkMode={darkMode} setDarkMode={setDarkMode} onReset={handleReset} />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {!analysisData ? (
          <UploadZone 
            onAnalysisComplete={handleAnalysisComplete}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        ) : (
          <Dashboard data={analysisData} onReset={handleReset} />
        )}
      </main>

      <footer className="text-center py-6 text-gray-600 dark:text-gray-400 text-sm">
        <p>Built with React, FastAPI, and AI • Portfolio Project</p>
      </footer>
    </div>
  )
}

export default App
