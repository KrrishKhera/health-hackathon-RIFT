import { useLocation, useNavigate } from 'react-router-dom'
import RiskBadge from '../components/RiskBadge'
import AccordionItem from '../components/ExpandableSection'
import ActionButtons from '../components/ActionButtons'

function ResultDashboard() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const result = state?.result

  if (!result) {
    navigate('/')
    return null
  }

  const points = result.llm_generated_explanation?.points || []

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-950 via-gray-950 to-gray-950 px-8 py-10 overflow-y-auto">
      
      {/* Top left project name */}
      <p className="text-white font-bold text-lg tracking-widest">VARIANTX</p>

      {/* Analysis done message */}
      <div className="flex flex-col items-center mt-12 mb-10">
        <h1 className="text-4xl font-bold text-white text-center">
          Analysis Complete
        </h1>
        <p className="text-gray-500 text-sm tracking-widest mt-2">
          results.ready.now
        </p>
      </div>

      {/* Risk Badge */}
      <div className="flex justify-center mb-10">
        <RiskBadge riskLabel={result.risk_assessment?.risk_label} />
      </div>

      {/* Expandable Sections */}
      <div className="max-w-4xl w-full mx-auto flex flex-col gap-3 mb-10">
        {points.length > 0 ? (
          points.map((point, index) => (
            <AccordionItem
              key={index}
              title={point.title}
              explanation={point.explanation}
            />
          ))
        ) : (
          <p className="text-gray-500 text-center text-sm">
            No detailed breakdown available.
          </p>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center mb-10">
        <ActionButtons data={result} />
      </div>

    </div>
  )
}

export default ResultDashboard