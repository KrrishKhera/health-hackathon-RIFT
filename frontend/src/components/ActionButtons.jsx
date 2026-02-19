import { useState } from 'react'

function ActionButtons({ data }) {
  const [copied, setCopied] = useState(false)

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${data.patient_id || 'pharma'}_report.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const handleCopy = async () => {
    await navigator.clipboard.writeText(JSON.stringify(data, null, 2))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex gap-4 justify-center">
      <button onClick={handleDownload}
        className="flex items-center gap-2 px-6 py-3 bg-pink-700 hover:bg-pink-600 text-white rounded-xl font-medium transition text-sm"
        style={{ fontFamily: "'Playfair Display', serif" }}>
        ↓ Download JSON
      </button>
      <button onClick={handleCopy}
        className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition text-sm ${
          copied ? 'bg-green-700 text-white' : 'bg-gray-700 hover:bg-gray-600 text-white'
        }`}
        style={{ fontFamily: "'Playfair Display', serif" }}>
        {copied ? '✓ Copied!' : '⧉ Copy JSON'}
      </button>
    </div>
  )
}

export default ActionButtons