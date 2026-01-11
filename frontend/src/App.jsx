import { useState, useEffect } from 'react'
import { Moon, Sun, ArrowUp } from 'lucide-react'
import UploadZone from './components/UploadZone'
import Dashboard from './components/Dashboard'
import Header from './components/Header'

function App() {
  const [darkMode, setDarkMode] = useState(true)
  const [analysisData, setAnalysisData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showBackToTop, setShowBackToTop] = useState(false)

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 400)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

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

      <footer className="text-center py-6 px-4 text-gray-600 dark:text-gray-400 text-xs md:text-sm">
        <p>Built with React, FastAPI, and AI • Portfolio Project</p>
      </footer>

      {showBackToTop && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-6 right-6 p-3 md:p-4 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg transition-all duration-300 z-40 min-h-[48px] min-w-[48px] flex items-center justify-center"
          aria-label="Back to top"
        >
          <ArrowUp className="w-5 h-5 md:w-6 md:h-6" />
        </button>
      )}
    </div>
  )
}

export default App
