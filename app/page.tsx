import TicTacToeGame from './components/TicTacToeGame'
import FeedbackSystem from './components/FeedbackSystem'

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="text-center mb-12">
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🎮 AI Tic-Tac-Toe Challenge
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Test your strategic thinking against advanced AI algorithms
          </p>
          <div className="grid md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl mb-2">🧠</div>
              <div className="font-semibold">Smart AI</div>
              <div className="text-sm text-gray-600">Multiple difficulty levels</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl mb-2">⚡</div>
              <div className="font-semibold">Real-time</div>
              <div className="text-sm text-gray-600">Instant AI responses</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl mb-2">📊</div>
              <div className="font-semibold">Statistics</div>
              <div className="text-sm text-gray-600">Track your progress</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl mb-2">🎯</div>
              <div className="font-semibold">Challenge</div>
              <div className="text-sm text-gray-600">From easy to expert</div>
            </div>
          </div>
        </div>
      </section>

      {/* Game Section */}
      <TicTacToeGame />

      {/* How to Play Section */}
      <section className="mt-16 mb-12">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center mb-6">🎯 How to Play</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-3">Game Rules</h3>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">1.</span>
                  You play as X, AI plays as O
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">2.</span>
                  Click any empty cell to make your move
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">3.</span>
                  Get 3 in a row (horizontal, vertical, or diagonal) to win
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">4.</span>
                  If all cells are filled with no winner, it's a tie
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-3">AI Difficulty Levels</h3>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">🟢</span>
                  <div>
                    <strong>Easy:</strong> Random moves, great for beginners
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-yellow-500 mr-2">🟡</span>
                  <div>
                    <strong>Medium:</strong> Strategic play with occasional mistakes
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-orange-500 mr-2">🟠</span>
                  <div>
                    <strong>Hard:</strong> Advanced strategy, rarely makes errors
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">🔴</span>
                  <div>
                    <strong>Expert:</strong> Perfect play using minimax algorithm
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* AI Technology Section */}
      <section className="mt-16 mb-12">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center mb-6">🤖 AI Technology</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-4">
              <div className="text-3xl mb-3">🧮</div>
              <h3 className="font-semibold mb-2">Minimax Algorithm</h3>
              <p className="text-sm text-gray-600">
                Expert level uses the minimax algorithm with alpha-beta pruning for perfect play
              </p>
            </div>
            <div className="text-center p-4">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="font-semibold mb-2">Strategic Heuristics</h3>
              <p className="text-sm text-gray-600">
                Medium and Hard levels use strategic heuristics like center control and corner preference
              </p>
            </div>
            <div className="text-center p-4">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="font-semibold mb-2">Real-time Processing</h3>
              <p className="text-sm text-gray-600">
                AI calculates moves in real-time with realistic thinking delays for better UX
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Feedback Section */}
      <FeedbackSystem />

      {/* Footer */}
      <footer className="mt-16 text-center py-8 border-t border-gray-200">
        <div className="text-gray-600">
          <p className="mb-2">
            🎮 AI Tic-Tac-Toe Challenge - Built with Next.js, React, and TypeScript
          </p>
          <p className="text-sm">
            Featuring multiple AI strategies from random play to perfect minimax algorithm
          </p>
        </div>
      </footer>
    </main>
  )
}