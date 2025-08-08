import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'AI Tic-Tac-Toe Challenge',
  description: 'Challenge advanced AI strategies in Tic-Tac-Toe. Multiple difficulty levels and intelligent opponents.',
  keywords: 'tic-tac-toe, AI, game, strategy, minimax, machine learning',
  authors: [{ name: 'AI Game Developer' }],
  openGraph: {
    title: 'AI Tic-Tac-Toe Challenge',
    description: 'Challenge advanced AI strategies in Tic-Tac-Toe',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen`}>
        <div className="container mx-auto px-4 py-8">
          <header className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              🎮 AI Tic-Tac-Toe Challenge
            </h1>
            <p className="text-gray-600 text-lg">
              Test your skills against advanced AI strategies
            </p>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}