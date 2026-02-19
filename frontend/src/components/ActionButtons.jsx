import { useState } from 'react'

function ActionButtons({ data }) {

  const handleDownload = () => {
    const jsonString = JSON.stringify(data, null, 2)
    const blob = new Blob([jsonString], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${data.patient_id}_report.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(JSON.stringify(data, null, 2))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex gap-4 justify-center mt-6">
      
      <button
        onClick={handleDownload}
        className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition"
      >
        ⬇ Download JSON
      </button>

      <button
        onClick={handleCopy}
        className="flex items-center gap-2 px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-xl font-medium transition"
      >
        {copied ? '✓ Copied!' : '⧉ Copy to Clipboard'}
      </button>

    </div>
  )
}

export default ActionButtons