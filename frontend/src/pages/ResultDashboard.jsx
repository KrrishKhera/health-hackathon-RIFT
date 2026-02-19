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

  useEffect(() => { if (!result) navigate('/') }, [result])
  if (!result) return null

  const llm = result.llm_generated_explanation || {}
  const profile = result.pharmacogenomic_profile || {}
  const risk = result.risk_assessment || {}
  const rec = result.clinical_recommendation || {}

  const subSections = [
    { title: 'Mechanism', explanation: llm.mechanism },
    { title: 'Variant Impact', explanation: llm.variant_impact },
    { title: 'Clinical Context', explanation: llm.clinical_context },
    { title: 'Alternative Options', explanation: llm.alternative_options },
    { title: 'Monitoring Parameters', explanation: llm.monitoring_parameters },
  ].filter(s => s.explanation)

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-950 via-gray-950 to-gray-950 px-6 py-10 overflow-y-auto"
      style={{ fontFamily: "'Lora', serif" }}>

      <div className="relative flex items-center justify-center mb-10">
        <button onClick={() => navigate('/')}
          className="absolute left-0 flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl transition text-sm"
          style={{ fontFamily: "'Lora', serif" }}>
          ← Back
        </button>
        <h1 className="text-4xl font-bold text-white"
          style={{ fontFamily: "'Playfair Display', serif", letterSpacing: '0.04em' }}>
          Variant-RX
        </h1>
      </div>

      <div className="flex flex-col items-center mb-10">
        <h2 className="text-3xl font-semibold text-white text-center"
          style={{ fontFamily: "'Playfair Display', serif", fontStyle: 'italic' }}>
          Analysis Complete
        </h2>
        <p className="text-gray-400 text-xs mt-2"
          style={{ fontFamily: "'Lora', serif", letterSpacing: '0.15em' }}>
          {result.patient_id} · {result.timestamp?.slice(0, 10)}
        </p>
      </div>

      {results.length > 1 && (
        <div className="flex gap-3 justify-center mb-8 flex-wrap">
          {results.map((r, i) => (
            <button key={i}
              onClick={() => { setActiveIndex(i); setSummaryOpen(false) }}
              className={`px-5 py-2 rounded-full text-sm transition ${
                activeIndex === i ? 'bg-pink-700 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
              style={{ fontFamily: "'Playfair Display', serif" }}>
              {r.drug}
            </button>
          ))}
        </div>
      )}

      <div className="flex justify-center mb-10">
        <RiskBadge riskLabel={risk.risk_label} severity={risk.severity} confidence={risk.confidence_score} />
      </div>

      <div className="max-w-3xl mx-auto mb-6 grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: 'Gene', value: profile.primary_gene },
          { label: 'Diplotype', value: profile.diplotype },
          { label: 'Phenotype', value: profile.phenotype },
          { label: 'Activity Score', value: rec.activity_score },
        ].map(({ label, value }) => (
          <div key={label} className="bg-gray-800/60 border border-gray-700 rounded-2xl px-4 py-4 text-center">
            <p className="text-gray-500 text-xs mb-2"
              style={{ fontFamily: "'Lora', serif", letterSpacing: '0.12em', textTransform: 'uppercase' }}>
              {label}
            </p>
            <p className="text-white font-semibold text-base"
              style={{ fontFamily: "'Playfair Display', serif" }}>
              {value ?? '—'}
            </p>
          </div>
        ))}
      </div>

      {rec.action && (
        <div className="max-w-3xl mx-auto mb-6 bg-gray-800/60 border border-gray-700 rounded-2xl px-6 py-5">
          <p className="text-gray-500 text-xs mb-2"
            style={{ fontFamily: "'Lora', serif", letterSpacing: '0.12em', textTransform: 'uppercase' }}>
            Recommendation
          </p>
          <p className="text-white text-sm leading-relaxed" style={{ fontFamily: "'Lora', serif" }}>
            {rec.action}
          </p>
          <p className="text-gray-600 text-xs mt-3" style={{ fontFamily: "'Lora', serif" }}>
            Source: {rec.guideline_source}
          </p>
        </div>
      )}

      <div className="max-w-3xl mx-auto mb-8">
        <div className="w-full border border-gray-700 rounded-2xl overflow-hidden">
          <div
            className="flex items-center justify-between px-6 py-5 bg-gray-800/60 cursor-pointer hover:bg-gray-700/60 transition"
            onClick={() => setSummaryOpen(!summaryOpen)}>
            <p className="text-gray-200 text-sm leading-relaxed flex-1 pr-4"
              style={{ fontFamily: "'Lora', serif", fontStyle: 'italic' }}>
              {llm.summary || 'Summary unavailable'}
            </p>
            <button
              className="w-7 h-7 rounded-full bg-gray-700 hover:bg-gray-600 text-white flex items-center justify-center flex-shrink-0 transition-transform duration-200"
              style={{ transform: summaryOpen ? 'rotate(45deg)' : 'rotate(0deg)' }}>
              +
            </button>
          </div>
          {summaryOpen && (
            <div className="bg-gray-950 px-4 py-4 flex flex-col gap-3">
              {subSections.length > 0 ? (
                subSections.map((section, index) => (
                  <ExpandableSection key={index} title={section.title} explanation={section.explanation} />
                ))
              ) : (
                <p className="text-gray-500 text-sm text-center">No detailed breakdown available.</p>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="flex justify-center mb-10">
        <ActionButtons data={result} />
      </div>
    </div>
  )
}

export default ResultDashboard