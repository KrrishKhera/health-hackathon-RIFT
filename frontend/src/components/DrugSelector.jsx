import { useState } from 'react'

const DRUGS = [
  'CODEINE',
  'WARFARIN',
  'CLOPIDOGREL',
  'SIMVASTATIN',
  'AZATHIOPRINE',
  'FLUOROURACIL'
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
      <p className="text-sm text-gray-400 mb-2">Select Drug(s)</p>
      <div className="grid grid-cols-3 gap-3">
        {DRUGS.map(drug => (
          <button
            key={drug}
            onClick={() => toggleDrug(drug)}
            className={`py-3 px-4 rounded-xl text-sm font-medium tracking-wide transition-colors duration-200
              ${selectedDrugs.includes(drug)
                ? 'bg-green-600 text-white border border-green-500'
                : 'bg-gray-800 text-gray-400 border border-gray-600 hover:border-gray-400'
              }`}
          >
            {drug}
          </button>
        ))}
      </div>

      {selectedDrugs.length > 0 && (
        <p className="text-xs text-gray-500 mt-2">
          {selectedDrugs.length} drug{selectedDrugs.length > 1 ? 's' : ''} selected
        </p>
      )}
    </div>
  )
}

export default DrugSelector