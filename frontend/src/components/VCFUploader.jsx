import { useState, useRef } from 'react'

const MAX_FILE_SIZE = 5 * 1024 * 1024

function VCFUploader({ onFileSelect }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [error, setError] = useState('')
  const [isValid, setIsValid] = useState(null)
  const inputRef = useRef(null)

  const validateFile = (file) => {
    if (!file.name.endsWith('.vcf')) {
      setError('Invalid file format')
      setIsValid(false)
      setSelectedFile(file)
      onFileSelect(null)
      return false
    }
    if (file.size > MAX_FILE_SIZE) {
      setError('File too large. Max 5MB')
      setIsValid(false)
      setSelectedFile(file)
      onFileSelect(null)
      return false
    }
    return true
  }

  const handleFile = (file) => {
    setError('')
    if (validateFile(file)) {
      setSelectedFile(file)
      setIsValid(true)
      onFileSelect(file)
    }
  }

  const handleInputChange = (e) => {
    const file = e.target.files[0]
    if (file) handleFile(file)
  }

  const handleClick = () => {
    inputRef.current.click()
  }

  return (
    <div className="w-full">
      <div className="flex items-center gap-4">
        
        {/* Label */}
        <p className="text-white font-semibold text-lg whitespace-nowrap">UPLOAD VCF FILE</p>

        {/* File display rectangle */}
        <div
          className={`flex-1 px-5 py-3 rounded-lg border text-base truncate
            ${isValid === null ? 'border-gray-600 text-gray-500' : ''}
            ${isValid === true ? 'border-green-500 text-green-300' : ''}
            ${isValid === false ? 'border-red-500 text-red-400' : ''}
            bg-gray-900
          `}
        >
          {selectedFile ? selectedFile.name : 'No file selected'}
        </div>

        {/* Plus button */}
        <button
          onClick={handleClick}
          className="w-9 h-9 rounded-full bg-gray-700 hover:bg-gray-600 text-white text-xl flex items-center justify-center transition"
        >
          +
        </button>

        <input
          ref={inputRef}
          type="file"
          accept=".vcf"
          onChange={handleInputChange}
          className="hidden"
        />

      </div>

      {/* Error message */}
      {error && (
        <p className="text-red-400 text-xs mt-1 ml-1">{error}</p>
      )}
    </div>
  )
}

export default VCFUploader