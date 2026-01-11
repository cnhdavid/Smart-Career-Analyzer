import { CheckCircle2 } from 'lucide-react'

function SkillsList({ skills }) {
  return (
    <div className="flex flex-wrap gap-2">
      {skills.slice(0, 10).map((skill, index) => (
        <span
          key={index}
          className="inline-flex items-center gap-1 px-2.5 py-1.5 md:px-3 md:py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-xs md:text-sm font-medium"
        >
          <CheckCircle2 className="w-3 h-3 flex-shrink-0" />
          <span className="truncate max-w-[150px]">{skill}</span>
        </span>
      ))}
      {skills.length > 10 && (
        <span className="inline-flex items-center px-2.5 py-1.5 md:px-3 md:py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full text-xs md:text-sm">
          +{skills.length - 10} more
        </span>
      )}
    </div>
  )
}

export default SkillsList
