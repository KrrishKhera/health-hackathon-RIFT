import { useState, useRef } from 'react'

const MAX_FILE_SIZE = 5 * 1024 * 1024

function VCFUploader({ onFileSelect }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [error, setError] = useState('')
  const [isValid, setIsValid] = useState(null)
  const inputRef = useRef(null)

  const validateFile = (file) => {
    if (!file.name.endsWith('.vcf')) {
      setError('Invalid file format — only .vcf allowed')
      setIsValid(false); setSelectedFile(file); onFileSelect(null)
      return false
    }
    if (file.size > MAX_FILE_SIZE) {
      setError('File too large — max 5MB')
      setIsValid(false); setSelectedFile(file); onFileSelect(null)
      return false
    }
    return true
  }

  const handleFile = (file) => {
    setError('')
    if (validateFile(file)) { setSelectedFile(file); setIsValid(true); onFileSelect(file) }
  }

  return (
    <div className="w-full">
      <p className="text-gray-400 text-xs mb-2"
        style={{ fontFamily: "'Lora', serif", letterSpacing: '0.18em', textTransform: 'uppercase' }}>
        Upload VCF File
      </p>
      <div
        onDrop={(e) => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleFile(f) }}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current.click()}
        className={`w-full flex items-center justify-between px-5 py-4 rounded-xl border cursor-pointer transition
          ${isValid === true ? 'border-green-500 bg-green-500/5' : ''}
          ${isValid === false ? 'border-red-500 bg-red-500/5' : ''}
          ${isValid === null ? 'border-gray-600 bg-gray-800/60 hover:border-gray-400' : ''}
        `}>
        <div className="flex items-center gap-3 overflow-hidden">
          <span className={`text-base flex-shrink-0 ${
            isValid === true ? 'text-green-400' : isValid === false ? 'text-red-400' : 'text-gray-500'}`}>
            {isValid === true ? '✓' : isValid === false ? '✕' : '↑'}
          </span>
          <span className={`text-sm truncate ${
            isValid === true ? 'text-green-300' : isValid === false ? 'text-red-400' : 'text-gray-500'}`}
            style={{ fontFamily: "'Lora', serif" }}>
            {selectedFile ? selectedFile.name : 'Drag & drop or click to upload .vcf file'}
          </span>
        </div>
        <span className="text-gray-600 text-xs flex-shrink-0 ml-4"
          style={{ fontFamily: "'Lora', serif", letterSpacing: '0.1em' }}>
          MAX 5MB
        </span>
      </div>
      <input ref={inputRef} type="file" accept=".vcf"
        onChange={(e) => { const f = e.target.files[0]; if (f) handleFile(f) }}
        className="hidden" />
      {error && (
        <p className="text-red-400 text-xs mt-2" style={{ fontFamily: "'Lora', serif" }}>{error}</p>
      )}
    </div>
  )
}

export default VCFUploader