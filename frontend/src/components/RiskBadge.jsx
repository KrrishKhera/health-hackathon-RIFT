const RISK_CONFIG = {
  'Safe':           { color: 'bg-green-600 border-green-500 text-white',  glow: 'shadow-lg shadow-green-500/30',  icon: '✓' },
  'Adjust Dosage':  { color: 'bg-yellow-500 border-yellow-400 text-black', glow: 'shadow-lg shadow-yellow-500/30', icon: '⚠' },
  'Toxic':          { color: 'bg-red-600 border-red-500 text-white',       glow: 'shadow-lg shadow-red-500/30',    icon: '✕' },
  'Ineffective':    { color: 'bg-orange-600 border-orange-500 text-white', glow: 'shadow-lg shadow-orange-500/30', icon: '⊘' },
  'Unknown':        { color: 'bg-gray-600 border-gray-500 text-white',     glow: '',                               icon: '?' },
}

function RiskBadge({ riskLabel, severity, confidence }) {
  const config = RISK_CONFIG[riskLabel] || RISK_CONFIG['Unknown']
  return (
    <div className="flex flex-col items-center gap-3">
      <p className="text-xs text-gray-400"
        style={{ fontFamily: "'Lora', serif", letterSpacing: '0.18em', textTransform: 'uppercase' }}>
        Risk Assessment
      </p>
      <div className={`flex items-center gap-3 px-8 py-3 rounded-full border-2 text-xl font-bold ${config.color} ${config.glow}`}
        style={{ fontFamily: "'Playfair Display', serif" }}>
        <span>{config.icon}</span>
        <span>{riskLabel}</span>
      </div>
      <div className="flex gap-5 text-xs text-gray-500" style={{ fontFamily: "'Lora', serif", letterSpacing: '0.1em' }}>
        {severity && (
          <span>Severity: <span className="text-gray-300 uppercase">{severity}</span></span>
        )}
        {confidence && (
          <span>Confidence: <span className="text-gray-300">{Math.round(confidence * 100)}%</span></span>
        )}
      </div>
    </div>
  )
}

export default RiskBadge