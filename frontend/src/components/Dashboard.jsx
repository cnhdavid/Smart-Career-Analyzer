import { RotateCcw, TrendingUp, Award, BookOpen, Target, Download, Sparkles, Briefcase, Zap, CheckCircle, AlertTriangle } from 'lucide-react'
import RadarChart from './RadarChart'
import RoleMatchCard from './RoleMatchCard'
import SkillsList from './SkillsList'
import Roadmap from './Roadmap'
import { generatePDF } from '../utils/pdfGenerator'

function Dashboard({ data, onReset }) {
  const topRole = Object.entries(data.role_matches).sort((a, b) => b[1] - a[1])[0]

  const handleDownloadReport = () => {
    generatePDF(data)
  }

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold mb-2">Your Career Analysis</h2>
          <p className="text-gray-600 dark:text-gray-400">
            {data.current_field && <span className="font-semibold text-primary-600">{data.current_field}</span>}
            {data.current_field && " • "}
            {data.skills.length} competencies detected • {data.experience_years} years experience
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleDownloadReport}
            className="btn-primary flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Download Report
          </button>
          <button
            onClick={onReset}
            className="btn-secondary flex items-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            Analyze Another
          </button>
        </div>
      </div>

      {data.summary && (
        <div className="card bg-gradient-to-br from-primary-50 to-purple-50 dark:from-primary-900/20 dark:to-purple-900/20 border-2 border-primary-200 dark:border-primary-800">
          <div className="flex items-start gap-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-2 text-primary-900 dark:text-primary-100">
                Professional Summary
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {data.summary}
              </p>
            </div>
          </div>
        </div>
      )}

      {data.ats_feedback && data.ats_feedback.length > 0 && (
        <div className="card bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-200 dark:border-green-800">
          <div className="flex items-start gap-3">
            <div className="bg-green-600 p-2 rounded-lg">
              <CheckCircle className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-3 text-green-900 dark:text-green-100">
                ATS Optimization Tips
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Applicant Tracking Systems (ATS) scan resumes before human eyes see them. Here's how to improve your resume's compatibility:
              </p>
              <div className="space-y-2">
                {data.ats_feedback.map((tip, index) => (
                  <div key={index} className="flex items-start gap-2 p-3 bg-white dark:bg-gray-800 rounded-lg border border-green-200 dark:border-green-700">
                    {tip.startsWith('⚠️') || tip.startsWith('📋') || tip.startsWith('📊') || tip.startsWith('🎯') ? (
                      <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                    ) : (
                      <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    )}
                    <p className="text-gray-700 dark:text-gray-300 text-sm">
                      {tip}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-primary-600" />
            <h3 className="text-xl font-semibold">Key Competencies Comparison</h3>
          </div>
          <RadarChart data={data.radar_data} />
        </div>

        <div className="space-y-4">
          <div className="card bg-gradient-to-br from-primary-600 to-purple-600 text-white">
            <div className="flex items-center gap-2 mb-2">
              <Award className="w-5 h-5" />
              <h3 className="text-lg font-semibold">Best Match</h3>
            </div>
            <p className="text-3xl font-bold mb-1">{topRole[0]}</p>
            <p className="text-xl opacity-90">{topRole[1]}% Match</p>
          </div>

          <div className="card">
            <div className="flex items-center gap-2 mb-3">
              <Briefcase className="w-5 h-5 text-primary-600" />
              <h3 className="text-lg font-semibold">Your Competencies</h3>
            </div>
            <SkillsList skills={data.skills} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {Object.entries(data.role_matches).map(([role, score]) => (
          <RoleMatchCard
            key={role}
            role={role}
            score={score}
            skillGaps={data.skill_gaps[role] || []}
          />
        ))}
      </div>

      {data.trending_industries && data.trending_industries.length > 0 && (
        <div className="card bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-purple-600" />
            <h3 className="text-xl font-semibold">Trending Industries for Your Profile</h3>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-3">
            Based on your skill set, these sectors are actively seeking professionals like you:
          </p>
          <div className="flex flex-wrap gap-2">
            {data.trending_industries.map((industry, index) => (
              <span
                key={index}
                className="px-4 py-2 bg-white dark:bg-gray-800 rounded-lg border-2 border-purple-200 dark:border-purple-700 text-purple-700 dark:text-purple-300 font-medium shadow-sm"
              >
                {industry}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5 text-primary-600" />
          <h3 className="text-xl font-semibold">Recommended Learning Path</h3>
        </div>
        <Roadmap recommendations={data.recommendations} />
      </div>
    </div>
  )
}

export default Dashboard
