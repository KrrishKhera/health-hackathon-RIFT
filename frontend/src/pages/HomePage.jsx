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
    if (!file) {
      setError('Please upload a VCF file.')
      return
    }
    if (selectedDrugs.length === 0) {
      setError('Please select at least one drug.')
      return
    }

    setError('')
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      selectedDrugs.forEach(drug => formData.append('drug', drug))

      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/analyze`,
        formData
      )

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
    <div className="min-h-screen bg-gradient-to-br from-pink-950 via-gray-950 to-gray-950 px-8 py-6 flex flex-col">

      {/* Top left project name */}
      <p className="text-white font-bold text-lg tracking-widest">VARIANTX</p>

      {/* Center content */}
      <div className="flex flex-col items-center mt-16 mb-12">
        {/* Big tagline */}
        <h1 className="text-4xl font-bold text-white text-center leading-tight">
          Predict. Personalize. Protect.
        </h1>

        {/* Smaller word.word.word tagline */}
        <p className="text-gray-500 text-sm tracking-widest mt-3">
          genomics.risk.precision
        </p>
      </div>

      {/* Upload and Drug selector card */}
      <div className="max-w-2xl w-full mx-auto flex flex-col gap-6">

        <VCFUploader onFileSelect={setFile} />
        <DrugSelector onDrugsChange={setSelectedDrugs} />

        {/* Error */}
        {error && (
          <p className="text-red-400 text-sm text-center">{error}</p>
        )}

        {/* Analyze button */}
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold tracking-wide transition mt-2"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

      </div>
    </div>
  )
}

export default HomePage