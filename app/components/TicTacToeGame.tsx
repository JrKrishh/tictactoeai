'use client'

import { useState, useEffect, useCallback } from 'react'

// AI Strategy Types
export enum AIStrategy {
  EASY = 'easy',
  MEDIUM = 'medium', 
  HARD = 'hard',
  EXPERT = 'expert'
}

// Game State Types
type Player = 'X' | 'O' | null
type Board = Player[]
type GameStatus = 'playing' | 'won' | 'tie'

interface GameState {
  board: Board
  currentPlayer: Player
  status: GameStatus
  winner: Player
  winningLine: number[]
  moveCount: number
}

interface GameSettings {
  aiGoesFirst: boolean
  playerSymbol: Player
  aiSymbol: Player
}

interface GameStats {
  playerWins: number
  aiWins: number
  ties: number
  totalGames: number
}

// AI Logic Implementation
class TicTacToeAI {
  private strategy: AIStrategy

  constructor(strategy: AIStrategy) {
    this.strategy = strategy
  }

  // Check for winner
  private checkWinner(board: Board): { winner: Player; line: number[] } {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
      [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
      [0, 4, 8], [2, 4, 6] // diagonals
    ]

    for (const line of lines) {
      const [a, b, c] = line
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return { winner: board[a], line }
      }
    }

    return { winner: null, line: [] }
  }

  // Get available moves
  private getAvailableMoves(board: Board): number[] {
    return board.map((cell, index) => cell === null ? index : -1)
               .filter(index => index !== -1)
  }

  // Minimax algorithm for expert AI
  private minimax(board: Board, depth: number, isMaximizing: boolean, alpha: number = -Infinity, beta: number = Infinity): number {
    const { winner } = this.checkWinner(board)
    
    if (winner === 'O') return 10 - depth // AI wins
    if (winner === 'X') return depth - 10 // Player wins
    if (this.getAvailableMoves(board).length === 0) return 0 // Tie

    if (isMaximizing) {
      let maxEval = -Infinity
      for (const move of this.getAvailableMoves(board)) {
        board[move] = 'O'
        const eval_score = this.minimax(board, depth + 1, false, alpha, beta)
        board[move] = null
        maxEval = Math.max(maxEval, eval_score)
        alpha = Math.max(alpha, eval_score)
        if (beta <= alpha) break
      }
      return maxEval
    } else {
      let minEval = Infinity
      for (const move of this.getAvailableMoves(board)) {
        board[move] = 'X'
        const eval_score = this.minimax(board, depth + 1, true, alpha, beta)
        board[move] = null
        minEval = Math.min(minEval, eval_score)
        beta = Math.min(beta, eval_score)
        if (beta <= alpha) break
      }
      return minEval
    }
  }

  // Get best move using minimax
  private getBestMove(board: Board): number {
    let bestScore = -Infinity
    let bestMove = -1

    for (const move of this.getAvailableMoves(board)) {
      board[move] = 'O'
      const score = this.minimax(board, 0, false)
      board[move] = null

      if (score > bestScore) {
        bestScore = score
        bestMove = move
      }
    }

    return bestMove
  }

  // Strategic move for medium difficulty
  private getStrategicMove(board: Board): number {
    const available = this.getAvailableMoves(board)
    
    // Check for winning move
    for (const move of available) {
      board[move] = 'O'
      if (this.checkWinner(board).winner === 'O') {
        board[move] = null
        return move
      }
      board[move] = null
    }

    // Check for blocking move
    for (const move of available) {
      board[move] = 'X'
      if (this.checkWinner(board).winner === 'X') {
        board[move] = null
        return move
      }
      board[move] = null
    }

    // Prefer center
    if (available.includes(4)) return 4

    // Prefer corners
    const corners = [0, 2, 6, 8].filter(pos => available.includes(pos))
    if (corners.length > 0) {
      return corners[Math.floor(Math.random() * corners.length)]
    }

    // Random available move
    return available[Math.floor(Math.random() * available.length)]
  }

  // Get AI move based on strategy
  public getMove(board: Board): number {
    const available = this.getAvailableMoves(board)
    
    if (available.length === 0) return -1

    switch (this.strategy) {
      case AIStrategy.EASY:
        // Random move with occasional mistakes
        return available[Math.floor(Math.random() * available.length)]
      
      case AIStrategy.MEDIUM:
        // Strategic but not perfect
        return Math.random() < 0.8 ? this.getStrategicMove(board) : 
               available[Math.floor(Math.random() * available.length)]
      
      case AIStrategy.HARD:
        // Strategic with some randomness
        return Math.random() < 0.9 ? this.getStrategicMove(board) : this.getBestMove(board)
      
      case AIStrategy.EXPERT:
        // Perfect play using minimax
        return this.getBestMove(board)
      
      default:
        return available[Math.floor(Math.random() * available.length)]
    }
  }
}

// Strategy descriptions
const strategyInfo = {
  [AIStrategy.EASY]: {
    name: '🟢 Easy',
    description: 'Random moves, perfect for beginners',
    difficulty: 1
  },
  [AIStrategy.MEDIUM]: {
    name: '🟡 Medium', 
    description: 'Strategic play with some mistakes',
    difficulty: 2
  },
  [AIStrategy.HARD]: {
    name: '🟠 Hard',
    description: 'Advanced strategy, rarely makes mistakes',
    difficulty: 3
  },
  [AIStrategy.EXPERT]: {
    name: '🔴 Expert',
    description: 'Perfect play using minimax algorithm',
    difficulty: 4
  }
}

export default function TicTacToeGame() {
  // Game settings
  const [gameSettings, setGameSettings] = useState<GameSettings>({
    aiGoesFirst: false,
    playerSymbol: 'X',
    aiSymbol: 'O'
  })

  // Game state
  const [gameState, setGameState] = useState<GameState>({
    board: Array(9).fill(null),
    currentPlayer: gameSettings.aiGoesFirst ? gameSettings.aiSymbol : gameSettings.playerSymbol,
    status: 'playing',
    winner: null,
    winningLine: [],
    moveCount: 0
  })

  const [aiStrategy, setAiStrategy] = useState<AIStrategy>(AIStrategy.MEDIUM)
  const [gameStats, setGameStats] = useState<GameStats>({
    playerWins: 0,
    aiWins: 0,
    ties: 0,
    totalGames: 0
  })
  const [isAiThinking, setIsAiThinking] = useState(false)
  const [gameHistory, setGameHistory] = useState<string[]>([])

  // Initialize AI
  const ai = new TicTacToeAI(aiStrategy)

  // Check for winner
  const checkGameEnd = useCallback((board: Board): { status: GameStatus; winner: Player; line: number[] } => {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
      [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
      [0, 4, 8], [2, 4, 6] // diagonals
    ]

    for (const line of lines) {
      const [a, b, c] = line
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        return { status: 'won', winner: board[a], line }
      }
    }

    if (board.every(cell => cell !== null)) {
      return { status: 'tie', winner: null, line: [] }
    }

    return { status: 'playing', winner: null, line: [] }
  }, [])

  // Handle player move
  const handleCellClick = (index: number) => {
    if (gameState.board[index] || gameState.status !== 'playing' || gameState.currentPlayer !== gameSettings.playerSymbol || isAiThinking) {
      return
    }

    const newBoard = [...gameState.board]
    newBoard[index] = gameSettings.playerSymbol

    const gameEnd = checkGameEnd(newBoard)
    
    setGameState(prev => ({
      ...prev,
      board: newBoard,
      currentPlayer: gameSettings.aiSymbol,
      status: gameEnd.status,
      winner: gameEnd.winner,
      winningLine: gameEnd.line,
      moveCount: prev.moveCount + 1
    }))

    // Add move to history
    setGameHistory(prev => [...prev, `Player (${gameSettings.playerSymbol}) plays position ${index + 1}`])

    // Update stats if game ended
    if (gameEnd.status !== 'playing') {
      updateGameStats(gameEnd.winner)
    }
  }

  // AI move effect
  useEffect(() => {
    if (gameState.currentPlayer === gameSettings.aiSymbol && gameState.status === 'playing') {
      setIsAiThinking(true)
      
      const aiMoveTimer = setTimeout(() => {
        const aiMove = ai.getMove([...gameState.board])
        
        if (aiMove !== -1) {
          const newBoard = [...gameState.board]
          newBoard[aiMove] = gameSettings.aiSymbol

          const gameEnd = checkGameEnd(newBoard)
          
          setGameState(prev => ({
            ...prev,
            board: newBoard,
            currentPlayer: gameSettings.playerSymbol,
            status: gameEnd.status,
            winner: gameEnd.winner,
            winningLine: gameEnd.line,
            moveCount: prev.moveCount + 1
          }))

          // Add AI move to history
          setGameHistory(prev => [...prev, `AI (${strategyInfo[aiStrategy].name}) plays position ${aiMove + 1}`])

          // Update stats if game ended
          if (gameEnd.status !== 'playing') {
            updateGameStats(gameEnd.winner)
          }
        }
        
        setIsAiThinking(false)
      }, 500 + Math.random() * 1000) // Random delay for realism

      return () => clearTimeout(aiMoveTimer)
    }
  }, [gameState.currentPlayer, gameState.status, ai, aiStrategy, checkGameEnd, gameSettings])

  // Handle AI first move when AI goes first
  useEffect(() => {
    if (gameSettings.aiGoesFirst && gameState.moveCount === 0 && gameState.status === 'playing') {
      // Small delay to show the board first
      const timer = setTimeout(() => {
        if (gameState.currentPlayer === gameSettings.aiSymbol) {
          // Trigger AI move by setting thinking state
          setIsAiThinking(true)
        }
      }, 1000)
      
      return () => clearTimeout(timer)
    }
  }, [gameSettings.aiGoesFirst, gameState.moveCount, gameState.status, gameState.currentPlayer, gameSettings.aiSymbol])

  // Update game statistics
  const updateGameStats = (winner: Player) => {
    setGameStats(prev => ({
      playerWins: prev.playerWins + (winner === gameSettings.playerSymbol ? 1 : 0),
      aiWins: prev.aiWins + (winner === gameSettings.aiSymbol ? 1 : 0),
      ties: prev.ties + (winner === null ? 1 : 0),
      totalGames: prev.totalGames + 1
    }))
  }

  // Reset game
  const resetGame = () => {
    const firstPlayer = gameSettings.aiGoesFirst ? gameSettings.aiSymbol : gameSettings.playerSymbol
    setGameState({
      board: Array(9).fill(null),
      currentPlayer: firstPlayer,
      status: 'playing',
      winner: null,
      winningLine: [],
      moveCount: 0
    })
    setGameHistory([])
    setIsAiThinking(false)
  }

  // Change AI strategy
  const changeStrategy = (strategy: AIStrategy) => {
    setAiStrategy(strategy)
    resetGame()
  }

  // Toggle who goes first
  const toggleFirstPlayer = () => {
    setGameSettings(prev => ({
      ...prev,
      aiGoesFirst: !prev.aiGoesFirst,
      playerSymbol: prev.aiGoesFirst ? 'X' : 'O',
      aiSymbol: prev.aiGoesFirst ? 'O' : 'X'
    }))
    // Reset game with new settings
    setTimeout(() => resetGame(), 100)
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Game Settings */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-center mb-4">Game Settings</h2>
        
        {/* Who Goes First Toggle */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-6">
          <div className="flex items-center justify-center space-x-4">
            <span className="text-lg font-semibold">Who goes first?</span>
            <button
              onClick={toggleFirstPlayer}
              className={`px-6 py-2 rounded-lg font-semibold transition-all duration-200 ${
                gameSettings.aiGoesFirst
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              {gameSettings.aiGoesFirst ? (
                <>🤖 AI goes first (AI: {gameSettings.aiSymbol}, You: {gameSettings.playerSymbol})</>
              ) : (
                <>👤 You go first (You: {gameSettings.playerSymbol}, AI: {gameSettings.aiSymbol})</>
              )}
            </button>
          </div>
        </div>

        {/* Strategy Selection */}
        <h3 className="text-xl font-bold text-center mb-4">Choose AI Difficulty</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(strategyInfo).map(([strategy, info]) => (
            <div
              key={strategy}
              className={`strategy-card ${aiStrategy === strategy ? 'selected' : ''}`}
              onClick={() => changeStrategy(strategy as AIStrategy)}
            >
              <div className="text-center">
                <div className="text-lg font-semibold mb-1">{info.name}</div>
                <div className="text-sm text-gray-600 mb-2">{info.description}</div>
                <div className="flex justify-center">
                  {Array.from({ length: 4 }, (_, i) => (
                    <div
                      key={i}
                      className={`w-2 h-2 rounded-full mx-0.5 ${
                        i < info.difficulty ? 'bg-blue-500' : 'bg-gray-300'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Game Board */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="text-center mb-4">
            <h3 className="text-xl font-bold mb-2">Game Board</h3>
            {gameState.status === 'playing' && (
              <p className="text-lg">
                {isAiThinking ? (
                  <span className="text-orange-600 animate-pulse">🤖 AI is thinking...</span>
                ) : gameState.currentPlayer === gameSettings.playerSymbol ? (
                  <span className="text-blue-600">Your turn ({gameSettings.playerSymbol})</span>
                ) : (
                  <span className="text-red-600">AI's turn ({gameSettings.aiSymbol})</span>
                )}
              </p>
            )}
            {gameState.status === 'won' && (
              <p className="text-xl font-bold">
                {gameState.winner === gameSettings.playerSymbol ? (
                  <span className="text-green-600">🎉 You Won!</span>
                ) : (
                  <span className="text-red-600">🤖 AI Won!</span>
                )}
              </p>
            )}
            {gameState.status === 'tie' && (
              <p className="text-xl font-bold text-yellow-600">🤝 It's a Tie!</p>
            )}
          </div>

          {/* Tic-Tac-Toe Grid */}
          <div className="grid grid-cols-3 gap-2 max-w-xs mx-auto mb-4">
            {gameState.board.map((cell, index) => (
              <button
                key={index}
                className={`game-cell ${
                  gameState.winningLine.includes(index) ? 'winning-cell' : ''
                } ${cell === gameSettings.playerSymbol ? 'player-x' : cell === gameSettings.aiSymbol ? 'player-o' : ''} ${
                  gameState.status !== 'playing' || isAiThinking ? 'disabled' : ''
                }`}
                onClick={() => handleCellClick(index)}
                disabled={gameState.status !== 'playing' || isAiThinking}
              >
                {cell && (
                  <span className="animate-bounce-in">
                    {cell}
                  </span>
                )}
              </button>
            ))}
          </div>

          <div className="text-center">
            <button
              onClick={resetGame}
              className="btn-primary mr-2"
            >
              🔄 New Game
            </button>
          </div>
        </div>

        {/* Game Stats & History */}
        <div className="space-y-6">
          {/* Statistics */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Game Statistics</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{gameStats.playerWins}</div>
                <div className="text-sm text-gray-600">Your Wins</div>
              </div>
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">{gameStats.aiWins}</div>
                <div className="text-sm text-gray-600">AI Wins</div>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">{gameStats.ties}</div>
                <div className="text-sm text-gray-600">Ties</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{gameStats.totalGames}</div>
                <div className="text-sm text-gray-600">Total Games</div>
              </div>
            </div>
            {gameStats.totalGames > 0 && (
              <div className="mt-4 text-center">
                <div className="text-sm text-gray-600">
                  Win Rate: {((gameStats.playerWins / gameStats.totalGames) * 100).toFixed(1)}%
                </div>
              </div>
            )}
          </div>

          {/* Move History */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Move History</h3>
            <div className="max-h-48 overflow-y-auto">
              {gameHistory.length === 0 ? (
                <p className="text-gray-500 text-center">No moves yet</p>
              ) : (
                <div className="space-y-1">
                  {gameHistory.map((move, index) => (
                    <div
                      key={index}
                      className="text-sm p-2 bg-gray-50 rounded flex justify-between"
                    >
                      <span>{move}</span>
                      <span className="text-gray-400">#{index + 1}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}