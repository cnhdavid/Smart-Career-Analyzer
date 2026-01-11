import { useState } from 'react'
import { CheckCircle2, XCircle, ExternalLink, BookOpen, X } from 'lucide-react'

function RoleMatchCard({ role, score, skillGaps }) {
  const [selectedSkill, setSelectedSkill] = useState(null)
  const [showModal, setShowModal] = useState(false)

  const handleSkillClick = (skill) => {
    setSelectedSkill(skill)
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setSelectedSkill(null)
  }

  const getYouTubeSearchUrl = (skill) => {
    return `https://www.youtube.com/results?search_query=${encodeURIComponent(skill + ' tutorial')}`
  }

  const getCourseraSearchUrl = (skill) => {
    return `https://www.coursera.org/search?query=${encodeURIComponent(skill)}`
  }

  const getSkillTip = (skill) => {
    const tips = {
      'Python': 'Start with basic syntax and data structures, then build small projects to solidify your understanding.',
      'JavaScript': 'Master the fundamentals before diving into frameworks - focus on ES6+ features and async programming.',
      'React': 'Build component-based thinking by creating reusable UI components and understanding the virtual DOM.',
      'Machine Learning': 'Begin with supervised learning algorithms and practice on real datasets from Kaggle.',
      'Deep Learning': 'Start with neural network basics and implement models from scratch before using high-level frameworks.',
      'Docker': 'Learn by containerizing your existing projects - start simple with single-container apps.',
      'Kubernetes': 'Master Docker first, then deploy a simple app to understand pods, services, and deployments.',
      'AWS': 'Get hands-on with the free tier - start with EC2, S3, and Lambda to understand core services.',
      'SQL': 'Practice writing queries daily on platforms like LeetCode or HackerRank to build muscle memory.',
      'TensorFlow': 'Follow official tutorials and implement classic models like CNNs and RNNs from scratch.',
      'PyTorch': 'Start with tensor operations and autograd, then build neural networks using nn.Module.',
      'Node.js': 'Build REST APIs and understand the event loop - async/await patterns are crucial.',
      'TypeScript': 'Learn type annotations gradually by converting existing JavaScript projects to TypeScript.',
      'Statistics': 'Focus on probability distributions and hypothesis testing - apply concepts to real-world data.',
      'Data Visualization': 'Start with basic charts in libraries like Matplotlib or Chart.js before advanced visualizations.',
      'CI/CD': 'Set up automated testing and deployment for a personal project using GitHub Actions or Jenkins.',
      'Git': 'Practice branching strategies and learn to resolve merge conflicts through hands-on experience.',
    }
    return tips[skill] || `Practice ${skill} through hands-on projects and online tutorials to build real-world experience.`
  }
  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600 dark:text-green-400'
    if (score >= 50) return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getProgressColor = (score) => {
    if (score >= 75) return 'bg-green-600'
    if (score >= 50) return 'bg-yellow-600'
    return 'bg-red-600'
  }

  return (
    <div className="card hover:shadow-xl transition-shadow">
      <h3 className="text-lg font-semibold mb-3">{role}</h3>
      
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600 dark:text-gray-400">Match Score</span>
          <span className={`text-2xl font-bold ${getScoreColor(score)}`}>
            {score}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${getProgressColor(score)}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      {skillGaps.length > 0 && (
        <div>
          <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            Skills to Develop:
          </p>
          <div className="space-y-1">
            {skillGaps.slice(0, 3).map((skill, index) => (
              <button
                key={index}
                onClick={() => handleSkillClick(skill)}
                className="w-full flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors cursor-pointer group"
              >
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0 group-hover:scale-110 transition-transform" />
                <span className="group-hover:underline">{skill}</span>
                <BookOpen className="w-3 h-3 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
              </button>
            ))}
          </div>
        </div>
      )}

      {showModal && selectedSkill && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={closeModal}>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-primary-600" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">{selectedSkill}</h3>
              </div>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Learning Tip:</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                {getSkillTip(selectedSkill)}
              </p>
            </div>
            
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300">Learn More:</h4>
              <a
                href={getYouTubeSearchUrl(selectedSkill)}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                <span className="text-sm font-medium">Search on YouTube</span>
              </a>
              <a
                href={getCourseraSearchUrl(selectedSkill)}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                <span className="text-sm font-medium">Search on Coursera</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default RoleMatchCard
