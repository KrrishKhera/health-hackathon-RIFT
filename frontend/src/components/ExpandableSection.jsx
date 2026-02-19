import { useState } from 'react'

function ExpandableSection({ title, explanation }) {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div className="w-full border border-gray-700 rounded-xl overflow-hidden">
      <div
        className="flex items-center justify-between px-5 py-4 bg-gray-800/60 cursor-pointer hover:bg-gray-700/60 transition"
        onClick={() => setIsOpen(!isOpen)}>
        <p className="text-white font-medium text-sm"
          style={{ fontFamily: "'Playfair Display', serif" }}>
          {title}
        </p>
        <button
          className="w-7 h-7 rounded-full bg-gray-700 hover:bg-gray-600 text-white flex items-center justify-center flex-shrink-0 transition-transform duration-200"
          style={{ transform: isOpen ? 'rotate(45deg)' : 'rotate(0deg)' }}>
          +
        </button>
      </div>
      {isOpen && (
        <div className="px-5 py-4 bg-gray-900 text-gray-300 text-sm leading-relaxed"
          style={{ fontFamily: "'Lora', serif" }}>
          {explanation}
        </div>
      )}
    </div>
  )
}

export default ExpandableSection