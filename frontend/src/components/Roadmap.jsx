import { Clock, TrendingUp, ExternalLink, Lightbulb } from 'lucide-react'

function Roadmap({ recommendations }) {
  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800'
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800'
      case 'low':
        return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800'
      default:
        return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-600'
    }
  }

  return (
    <div className="space-y-4">
      {recommendations.map((rec, index) => (
        <div
          key={index}
          className="border border-gray-200 dark:border-gray-700 rounded-lg p-3 md:p-4 hover:shadow-md transition-shadow bg-gray-50 dark:bg-gray-800/50"
        >
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-2 gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-1">
                <h4 className="font-semibold text-base md:text-lg">{rec.skill}</h4>
                <span className={`px-2 py-1 rounded text-xs font-medium border ${getPriorityColor(rec.priority)} inline-block w-fit`}>
                  {rec.priority} Priority
                </span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-xs md:text-sm mb-3">
                {rec.resource}
              </p>
            </div>
          </div>
          
          {rec.learning_tip && (
            <div className="mb-3 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg border border-primary-200 dark:border-primary-800">
              <div className="flex items-start gap-2">
                <Lightbulb className="w-4 h-4 text-primary-600 dark:text-primary-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {rec.learning_tip}
                </p>
              </div>
            </div>
          )}
          
          <div className="flex flex-wrap items-center gap-3 md:gap-4 text-xs md:text-sm text-gray-600 dark:text-gray-400">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4 flex-shrink-0" />
              <span>{rec.timeframe}</span>
            </div>
            <div className="flex items-center gap-1">
              <TrendingUp className="w-4 h-4 flex-shrink-0" />
              <span className="hidden sm:inline">Skill Development</span>
              <span className="sm:hidden">Development</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default Roadmap
