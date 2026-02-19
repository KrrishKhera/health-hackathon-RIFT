import { useState } from 'react'

const DRUGS = [
  { name: 'CODEINE', gene: 'CYP2D6' },
  { name: 'WARFARIN', gene: 'CYP2C9' },
  { name: 'CLOPIDOGREL', gene: 'CYP2C19' },
  { name: 'SIMVASTATIN', gene: 'SLCO1B1' },
  { name: 'AZATHIOPRINE', gene: 'TPMT' },
  { name: 'FLUOROURACIL', gene: 'DPYD' },
]

function DrugSelector({ onDrugsChange }) {
  const [selectedDrugs, setSelectedDrugs] = useState([])

  const toggleDrug = (drug) => {
    const updated = selectedDrugs.includes(drug)
      ? selectedDrugs.filter(d => d !== drug)
      : [...selectedDrugs, drug]
    setSelectedDrugs(updated)
    onDrugsChange(updated)
  }

  return (
    <div className="w-full">
      <p className="text-gray-400 text-xs mb-2"
        style={{ fontFamily: "'Lora', serif", letterSpacing: '0.18em', textTransform: 'uppercase' }}>
        Select Drug(s)
      </p>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {DRUGS.map(({ name, gene }) => (
          <button key={name} onClick={() => toggleDrug(name)}
            className={`py-3 px-4 rounded-xl text-sm font-medium transition-colors duration-200 text-left
              ${selectedDrugs.includes(name)
                ? 'bg-pink-700 text-white border border-pink-500'
                : 'bg-gray-800/60 text-gray-400 border border-gray-600 hover:border-gray-400 hover:text-gray-200'
              }`}>
            <span className="block font-semibold" style={{ fontFamily: "'Playfair Display', serif" }}>{name}</span>
            <span className="block text-xs mt-0.5 opacity-60" style={{ fontFamily: "'Lora', serif", letterSpacing: '0.05em' }}>{gene}</span>
          </button>
        ))}
      </div>
      {selectedDrugs.length > 0 && (
        <p className="text-xs text-gray-500 mt-2" style={{ fontFamily: "'Lora', serif" }}>
          {selectedDrugs.length} drug{selectedDrugs.length > 1 ? 's' : ''} selected
        </p>
      )}
    </div>
  )
}

export default DrugSelector