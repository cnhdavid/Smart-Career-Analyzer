import { jsPDF } from 'jspdf'

export const generatePDF = (data) => {
  const doc = new jsPDF()
  
  const primaryColor = [99, 102, 241]
  const textColor = [31, 41, 55]
  const lightGray = [156, 163, 175]
  
  doc.setFontSize(24)
  doc.setTextColor(...primaryColor)
  doc.text('Career Analysis Report', 20, 20)
  
  doc.setFontSize(10)
  doc.setTextColor(...lightGray)
  doc.text(`Generated on ${new Date().toLocaleDateString()}`, 20, 28)
  
  doc.setDrawColor(...primaryColor)
  doc.setLineWidth(0.5)
  doc.line(20, 32, 190, 32)
  
  doc.setFontSize(12)
  doc.setTextColor(...textColor)
  doc.text('Professional Summary', 20, 42)
  doc.setFontSize(10)
  const summaryLines = doc.splitTextToSize(data.summary || 'No summary available', 170)
  doc.text(summaryLines, 20, 48)
  
  let yPos = 48 + (summaryLines.length * 5) + 10
  
  doc.setFontSize(12)
  doc.setTextColor(...textColor)
  doc.text('Profile Overview', 20, yPos)
  yPos += 8
  
  doc.setFontSize(10)
  if (data.current_field) {
    doc.text(`Current Field: ${data.current_field}`, 25, yPos)
    yPos += 6
  }
  doc.text(`Competencies Identified: ${data.skills.length}`, 25, yPos)
  yPos += 6
  doc.text(`Years of Experience: ${data.experience_years}`, 25, yPos)
  yPos += 6
  doc.text(`Key Skills: ${data.skills.slice(0, 10).join(', ')}${data.skills.length > 10 ? '...' : ''}`, 25, yPos)
  yPos += 10
  
  doc.setFontSize(12)
  doc.setTextColor(...textColor)
  doc.text('Role Match Scores', 20, yPos)
  yPos += 8
  
  const sortedRoles = Object.entries(data.role_matches).sort((a, b) => b[1] - a[1])
  sortedRoles.forEach(([role, score]) => {
    doc.setFontSize(10)
    doc.setTextColor(...textColor)
    doc.text(`${role}:`, 25, yPos)
    doc.setTextColor(...primaryColor)
    doc.text(`${score}%`, 120, yPos)
    
    doc.setFillColor(...primaryColor)
    const barWidth = (score / 100) * 60
    doc.rect(130, yPos - 3, barWidth, 4, 'F')
    
    yPos += 7
  })
  
  yPos += 5
  
  if (yPos > 250) {
    doc.addPage()
    yPos = 20
  }
  
  doc.setFontSize(12)
  doc.setTextColor(...textColor)
  doc.text('Skills to Develop', 20, yPos)
  yPos += 8
  
  sortedRoles.forEach(([role, score]) => {
    if (yPos > 270) {
      doc.addPage()
      yPos = 20
    }
    
    const gaps = data.skill_gaps[role] || []
    if (gaps.length > 0) {
      doc.setFontSize(10)
      doc.setFont(undefined, 'bold')
      doc.setTextColor(...textColor)
      doc.text(`${role}:`, 25, yPos)
      doc.setFont(undefined, 'normal')
      yPos += 6
      
      gaps.slice(0, 5).forEach(skill => {
        doc.setTextColor(...lightGray)
        doc.text(`• ${skill}`, 30, yPos)
        yPos += 5
      })
      yPos += 3
    }
  })
  
  if (yPos > 250) {
    doc.addPage()
    yPos = 20
  }
  
  if (data.trending_industries && data.trending_industries.length > 0) {
    doc.setFontSize(12)
    doc.setTextColor(...textColor)
    doc.text('Trending Industries for Your Profile', 20, yPos)
    yPos += 8
    
    doc.setFontSize(10)
    doc.setTextColor(...lightGray)
    data.trending_industries.forEach(industry => {
      doc.text(`• ${industry}`, 25, yPos)
      yPos += 5
    })
    yPos += 8
    
    if (yPos > 250) {
      doc.addPage()
      yPos = 20
    }
  }
  
  doc.setFontSize(12)
  doc.setTextColor(...textColor)
  doc.text('Learning Recommendations', 20, yPos)
  yPos += 8
  
  data.recommendations.forEach((rec, index) => {
    if (yPos > 260) {
      doc.addPage()
      yPos = 20
    }
    
    doc.setFontSize(10)
    doc.setFont(undefined, 'bold')
    doc.setTextColor(...primaryColor)
    doc.text(`${index + 1}. ${rec.skill}`, 25, yPos)
    doc.setFont(undefined, 'normal')
    yPos += 6
    
    doc.setTextColor(...textColor)
    doc.text(`Priority: ${rec.priority}`, 30, yPos)
    yPos += 5
    doc.text(`Resource: ${rec.resource}`, 30, yPos)
    yPos += 5
    doc.text(`Timeframe: ${rec.timeframe}`, 30, yPos)
    yPos += 5
    
    if (rec.learning_tip) {
      doc.setTextColor(...lightGray)
      const tipLines = doc.splitTextToSize(`Tip: ${rec.learning_tip}`, 160)
      doc.text(tipLines, 30, yPos)
      yPos += tipLines.length * 5
    }
    
    yPos += 5
  })
  
  doc.setFontSize(8)
  doc.setTextColor(...lightGray)
  const pageCount = doc.internal.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.text(`Page ${i} of ${pageCount}`, 180, 285)
    doc.text('Smart Portfolio Analyzer', 20, 285)
  }
  
  doc.save('career-analysis-report.pdf')
}
