const RISK_CONFIG = {
  'Safe': {
    color: 'bg-green-600 border-green-500 text-white',
    glow: 'shadow-green-500/40',
    icon: '✓'
  },
  'Adjust Dosage': {
    color: 'bg-yellow-500 border-yellow-400 text-black',
    glow: 'shadow-yellow-500/40',
    icon: '⚠'
  },
  'Toxic': {
    color: 'bg-red-600 border-red-500 text-white',
    glow: 'shadow-red-500/40',
    icon: '✕'
  },
  'Ineffective': {
    color: 'bg-red-600 border-red-500 text-white',
    glow: 'shadow-red-500/40',
    icon: '✕'
  },
  'Unknown': {
    color: 'bg-gray-600 border-gray-500 text-white',
    glow: 'shadow-gray-500/40',
    icon: '?'
  }
}

function RiskBadge({ riskLabel }) {
  const config = RISK_CONFIG[riskLabel] || RISK_CONFIG['Unknown']

  return (
    <div className="flex flex-col items-center gap-2">
      <p className="text-sm text-gray-400">Risk Assessment</p>
      <div
        className={`flex items-center gap-2 px-6 py-3 rounded-full border-2 text-lg font-bold shadow-lg ${config.color} ${config.glow}`}
      >
        <span>{config.icon}</span>
        <span>{riskLabel}</span>
      </div>
    </div>
  )
}

export default RiskBadge