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

      {/* Project name */}
      <h1 className="text-5xl font-bold text-white tracking-widest text-center w-full">Variant-RX</h1>

      {/* Tagline */}
      <div className="flex flex-col items-center mt-20">
        <h2 className="text-4xl font-bold text-white text-center leading-tight whitespace-nowrap">
          Transforming Genetic Data into Safer Prescriptions.
        </h2>
      </div>

      {/* word.word.word */}
      <p className="text-gray-400 text-base tracking-widest text-center mt-6">
        Predict. Prevent. Personalize.
      </p>

      {/* Upload and Drug selector */}
      <div className="max-w-4xl w-full mx-auto flex flex-col gap-10 mt-24">

        <VCFUploader onFileSelect={setFile} />
        <DrugSelector onDrugsChange={setSelectedDrugs} />

        {error && (
          <p className="text-red-400 text-sm text-center">{error}</p>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full py-4 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-semibold tracking-wide transition text-lg"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>

      </div>
    </div>
  )
}

export default HomePage