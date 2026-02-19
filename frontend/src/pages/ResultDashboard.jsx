import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import RiskBadge from '../components/RiskBadge'
import ExpandableSection from '../components/ExpandableSection'
import ActionButtons from '../components/ActionButtons'

function ResultDashboard() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const [activeIndex, setActiveIndex] = useState(0)
  const [summaryOpen, setSummaryOpen] = useState(false)

  const results = state?.results || []
  const result = results[activeIndex]

  useEffect(() => {
  if (!result) {
    navigate('/')
  }
  }, [result])

  if (!result) return null

  const llm = result.llm_generated_explanation || {}

  const subSections = [
    { title: "Mechanism", explanation: llm.mechanism },
    { title: "Variant Impact", explanation: llm.variant_impact },
    { title: "Clinical Context", explanation: llm.clinical_context },
    { title: "Alternative Options", explanation: llm.alternative_options },
    { title: "Monitoring Parameters", explanation: llm.monitoring_parameters },
  ].filter(s => s.explanation)

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-950 via-gray-950 to-gray-950 px-8 py-10 overflow-y-auto">

      {/* Top left project name */}
      <h1 className="text-5xl font-bold text-white tracking-widest text-center cursor-pointer transition">
        VARIANTRX
      </h1>

      <button onClick={() => navigate('/')}
        className="absolute top-3 left-8 flex items-center gap-2 px-3 py-3 hover:bg-gray-600 text-white rounded-xl font-medium transition"
      >
        ← Back
      </button>

      {/* Analysis Complete */}
      <div className="flex flex-col items-center mt-12 mb-6">
        <h1 className="text-5xl font-bold text-white text-center">
          ANALYSIS COMPLETE!
        </h1>
      </div>

      {/* Drug Tabs — only show if multiple drugs */}
      {results.length > 1 && (
        <div className="flex gap-5 justify-center mb-8">
          {results.map((r, i) => (
            <button
              key={i}
              onClick={() => {
                setActiveIndex(i)
                setSummaryOpen(false)
              }}
              className={`px-4 py-2 rounded-full text-sm font-medium transition
                ${activeIndex === i
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
            >
              {r.drug}
            </button>
          ))}
        </div>
      )}

      {/* Risk Badge */}
      <div className="flex justify-center mb-10">
        <RiskBadge riskLabel={result.risk_assessment?.risk_label} />
      </div>

      {/* Summary + Expandable Sections */}
      <div className="w-full px-10 mb-10">
        <div className="w-full border border-gray-700 rounded-xl overflow-hidden">

          {/* Summary Bar */}
          <div
            className="flex items-center justify-between px-5 py-4 bg-gray-800 cursor-pointer hover:bg-gray-750"
            onClick={() => setSummaryOpen(!summaryOpen)}
          >
            <p className="text-white font-medium flex-1 pr-4">
              {llm.summary || 'Summary unavailable'}
            </p>
            <button
              className="w-7 h-7 rounded-full bg-gray-700 hover:bg-gray-600 text-white flex items-center justify-center flex-shrink-0 transition-transform duration-200"
              style={{ transform: summaryOpen ? 'rotate(45deg)' : 'rotate(0deg)' }}
            >
              +
            </button>
          </div>

          {/* Sub sections dropdown */}
          {summaryOpen && (
            <div className="bg-gray-950 px-4 py-4 flex flex-col gap-3">
              {subSections.length > 0 ? (
                subSections.map((section, index) => (
                  <ExpandableSection
                    key={index}
                    title={section.title}
                    explanation={section.explanation}
                  />
                ))
              ) : (
                <p className="text-gray-500 text-sm text-center">
                  No detailed breakdown available.
                </p>
              )}
            </div>
          )}

        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center mb-10">
        <ActionButtons data={result} />
      </div>

    </div>
  )
}

export default ResultDashboard