import { Radar, RadarChart as RechartsRadar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts'

function RadarChart({ data }) {
  const chartData = data.labels.map((label, index) => ({
    category: label,
    yourSkills: data.datasets[0].data[index],
    industry: data.datasets[1].data[index],
  }))

  return (
    <ResponsiveContainer width="100%" height={400}>
      <RechartsRadar data={chartData}>
        <PolarGrid stroke="#374151" className="dark:stroke-gray-600" />
        <PolarAngleAxis 
          dataKey="category" 
          tick={{ fill: '#6B7280', fontSize: 12 }}
          className="dark:fill-gray-400"
        />
        <PolarRadiusAxis 
          angle={90} 
          domain={[0, 100]}
          tick={{ fill: '#6B7280', fontSize: 10 }}
        />
        <Radar
          name="Your Skills"
          dataKey="yourSkills"
          stroke="#0ea5e9"
          fill="#0ea5e9"
          fillOpacity={0.6}
        />
        <Radar
          name="Industry Standard"
          dataKey="industry"
          stroke="#8b5cf6"
          fill="#8b5cf6"
          fillOpacity={0.3}
        />
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }}
          iconType="circle"
        />
      </RechartsRadar>
    </ResponsiveContainer>
  )
}

export default RadarChart
