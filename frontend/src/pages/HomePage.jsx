import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import VCFUploader from '../components/VCFUploader'
import DrugSelector from '../components/DrugSelector'

function HomePage() {
  const [file, setFile] = useState(null)
  const [selectedDrugs, setSelectedDrugs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleAnalyze = async () => {
    if (!file) { setError('Please upload a .vcf file.'); return }
    if (selectedDrugs.length === 0) { setError('Please select at least one drug.'); return }
    setError('')
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      selectedDrugs.forEach(drug => formData.append('drug', drug))
      const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/analyze`, formData)
      const data = response.data
      const results = Array.isArray(data) ? data : [data]
      navigate('/dashboard', { state: { results } })
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-950 via-gray-950 to-gray-950 px-8 py-12 flex flex-col"
      style={{ fontFamily: "'Lora', serif" }}>

      <h1 className="text-5xl font-bold text-white text-center w-full"
        style={{ fontFamily: "'Playfair Display', serif", letterSpacing: '0.04em' }}>
        Variant-RX
      </h1>

      <div className="flex flex-col items-center mt-14 mb-16">
        <h2 className="text-3xl font-normal text-white text-center leading-snug max-w-2xl"
          style={{ fontFamily: "'Playfair Display', serif", fontStyle: 'italic' }}>
          Transforming Genetic Data into Safer Prescriptions.
        </h2>
        <p className="text-gray-500 text-xs text-center mt-4"
          style={{ fontFamily: "'Lora', serif", letterSpacing: '0.2em' }}>
          Predict · Prevent · Personalize
        </p>
      </div>

      <div className="max-w-3xl w-full mx-auto flex flex-col gap-8">
        <VCFUploader onFileSelect={setFile} />
        <DrugSelector onDrugsChange={setSelectedDrugs} />

        {file && selectedDrugs.length > 0 && !error && (
          <p className="text-green-400 text-sm text-center" style={{ fontFamily: "'Lora', serif" }}>
            Ready — {file.name} · {selectedDrugs.length} drug{selectedDrugs.length > 1 ? 's' : ''} selected
          </p>
        )}

        {error && (
          <p className="text-red-400 text-sm text-center" style={{ fontFamily: "'Lora', serif" }}>{error}</p>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full py-4 rounded-xl bg-pink-700 hover:bg-pink-600 disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold tracking-wide transition"
          style={{ fontFamily: "'Playfair Display', serif", fontSize: '1.1rem' }}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Analysing...
            </span>
          ) : 'Analyze'}
        </button>
      </div>
    </div>
  )
}

export default HomePage