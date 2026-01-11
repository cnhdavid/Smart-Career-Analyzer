import { Moon, Sun, Brain, RotateCcw } from 'lucide-react'

function Header({ darkMode, setDarkMode, onReset }) {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-md border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 py-3 md:py-4 max-w-7xl">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 md:gap-3 min-w-0 flex-1">
            <div className="bg-primary-600 p-1.5 md:p-2 rounded-lg flex-shrink-0">
              <Brain className="w-5 h-5 md:w-6 md:h-6 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="text-lg sm:text-xl md:text-2xl font-bold text-gray-900 dark:text-white truncate">
                Smart Career Analyzer
              </h1>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 hidden sm:block">
                AI-Powered Skill Gap Analysis
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2 md:gap-3 flex-shrink-0">
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <Sun className="w-5 h-5 text-yellow-500" />
              ) : (
                <Moon className="w-5 h-5 text-gray-700" />
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
