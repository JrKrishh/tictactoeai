'use client'

import { useState } from 'react'

interface Feedback {
  id: string
  rating: number
  difficulty: string
  experience: string
  suggestions: string
  timestamp: string
}

interface FeedbackStats {
  totalFeedbacks: number
  averageRating: number
  difficultyDistribution: Record<string, number>
  recentFeedbacks: Feedback[]
}

export default function FeedbackSystem() {
  const [showFeedbackForm, setShowFeedbackForm] = useState(false)
  const [feedback, setFeedback] = useState({
    rating: 5,
    difficulty: '',
    experience: '',
    suggestions: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitMessage, setSubmitMessage] = useState('')
  const [feedbackStats, setFeedbackStats] = useState<FeedbackStats>({
    totalFeedbacks: 0,
    averageRating: 0,
    difficultyDistribution: {},
    recentFeedbacks: []
  })

  // Load feedback stats from localStorage
  const loadFeedbackStats = () => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('tictactoe-feedback-stats')
      if (stored) {
        setFeedbackStats(JSON.parse(stored))
      }
    }
  }

  // Save feedback stats to localStorage
  const saveFeedbackStats = (stats: FeedbackStats) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('tictactoe-feedback-stats', JSON.stringify(stats))
      setFeedbackStats(stats)
    }
  }

  // Submit feedback
  const handleSubmitFeedback = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // Create feedback object
      const newFeedback: Feedback = {
        id: Date.now().toString(),
        rating: feedback.rating,
        difficulty: feedback.difficulty,
        experience: feedback.experience,
        suggestions: feedback.suggestions,
        timestamp: new Date().toISOString()
      }

      // Send feedback to API (which will email it)
      const apiResponse = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rating: feedback.rating,
          difficulty: feedback.difficulty,
          experience: feedback.experience,
          suggestions: feedback.suggestions,
          timestamp: newFeedback.timestamp
        })
      })

      const apiResult = await apiResponse.json()

      // Load current stats
      const currentStats = typeof window !== 'undefined' 
        ? JSON.parse(localStorage.getItem('tictactoe-feedback-stats') || '{"totalFeedbacks":0,"averageRating":0,"difficultyDistribution":{},"recentFeedbacks":[]}')
        : { totalFeedbacks: 0, averageRating: 0, difficultyDistribution: {}, recentFeedbacks: [] }

      // Update stats
      const newTotalFeedbacks = currentStats.totalFeedbacks + 1
      const newAverageRating = ((currentStats.averageRating * currentStats.totalFeedbacks) + feedback.rating) / newTotalFeedbacks
      
      const newDifficultyDistribution = { ...currentStats.difficultyDistribution }
      newDifficultyDistribution[feedback.difficulty] = (newDifficultyDistribution[feedback.difficulty] || 0) + 1

      const newRecentFeedbacks = [newFeedback, ...currentStats.recentFeedbacks].slice(0, 10) // Keep only last 10

      const updatedStats: FeedbackStats = {
        totalFeedbacks: newTotalFeedbacks,
        averageRating: newAverageRating,
        difficultyDistribution: newDifficultyDistribution,
        recentFeedbacks: newRecentFeedbacks
      }

      // Save to localStorage
      saveFeedbackStats(updatedStats)

      // Show success message with email status
      if (apiResult.success) {
        setSubmitMessage(
          apiResult.emailSent 
            ? 'Thank you for your feedback! 📧 Email sent successfully! 🎉'
            : 'Thank you for your feedback! 🎉 (Email delivery pending)'
        )
      } else {
        setSubmitMessage('Feedback received, but there was an issue with email delivery. We still got your feedback! 📝')
      }

      setFeedback({ rating: 5, difficulty: '', experience: '', suggestions: '' })
      setShowFeedbackForm(false)

      // Clear success message after 5 seconds
      setTimeout(() => setSubmitMessage(''), 5000)

    } catch (error) {
      console.error('Feedback submission error:', error)
      setSubmitMessage('Error submitting feedback. Please try again. 😔')
    } finally {
      setIsSubmitting(false)
    }
  }

  // Load stats on component mount
  useState(() => {
    loadFeedbackStats()
  })

  return (
    <div className="max-w-4xl mx-auto mt-12">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            💬 Share Your Experience
          </h2>
          <p className="text-gray-600">
            Help us improve the AI Tic-Tac-Toe experience
          </p>
        </div>

        {/* Success Message */}
        {submitMessage && (
          <div className={`mb-4 p-4 rounded-lg text-center ${
            submitMessage.includes('Error') 
              ? 'bg-red-100 text-red-700 border border-red-300'
              : 'bg-green-100 text-green-700 border border-green-300'
          }`}>
            {submitMessage}
          </div>
        )}

        {/* Feedback Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{feedbackStats.totalFeedbacks}</div>
            <div className="text-sm text-gray-600">Total Feedbacks</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-3xl font-bold text-yellow-600">
              {feedbackStats.averageRating.toFixed(1)}⭐
            </div>
            <div className="text-sm text-gray-600">Average Rating</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-3xl font-bold text-green-600">
              {Object.keys(feedbackStats.difficultyDistribution).length}
            </div>
            <div className="text-sm text-gray-600">Difficulty Levels Tried</div>
          </div>
        </div>

        {/* Feedback Form Toggle */}
        <div className="text-center mb-6">
          <button
            onClick={() => setShowFeedbackForm(!showFeedbackForm)}
            className="btn-primary"
          >
            {showFeedbackForm ? '❌ Cancel Feedback' : '📝 Give Feedback'}
          </button>
        </div>

        {/* Feedback Form */}
        {showFeedbackForm && (
          <form onSubmit={handleSubmitFeedback} className="feedback-form mb-8">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Rating */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Overall Rating
                </label>
                <div className="flex items-center space-x-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setFeedback(prev => ({ ...prev, rating: star }))}
                      className={`text-2xl ${
                        star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'
                      } hover:text-yellow-400 transition-colors`}
                    >
                      ⭐
                    </button>
                  ))}
                  <span className="ml-2 text-sm text-gray-600">
                    ({feedback.rating}/5)
                  </span>
                </div>
              </div>

              {/* Difficulty Level */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Which difficulty did you enjoy most?
                </label>
                <select
                  value={feedback.difficulty}
                  onChange={(e) => setFeedback(prev => ({ ...prev, difficulty: e.target.value }))}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select difficulty</option>
                  <option value="easy">🟢 Easy</option>
                  <option value="medium">🟡 Medium</option>
                  <option value="hard">🟠 Hard</option>
                  <option value="expert">🔴 Expert</option>
                </select>
              </div>
            </div>

            {/* Experience */}
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                How was your gaming experience?
              </label>
              <textarea
                value={feedback.experience}
                onChange={(e) => setFeedback(prev => ({ ...prev, experience: e.target.value }))}
                placeholder="Tell us about your experience playing against the AI..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                required
              />
            </div>

            {/* Suggestions */}
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Suggestions for improvement (optional)
              </label>
              <textarea
                value={feedback.suggestions}
                onChange={(e) => setFeedback(prev => ({ ...prev, suggestions: e.target.value }))}
                placeholder="Any features you'd like to see or improvements you'd suggest..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
            </div>

            {/* Submit Button */}
            <div className="mt-6 text-center">
              <button
                type="submit"
                disabled={isSubmitting}
                className={`btn-success ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {isSubmitting ? '⏳ Submitting...' : '🚀 Submit Feedback'}
              </button>
            </div>
          </form>
        )}

        {/* Recent Feedbacks */}
        {feedbackStats.recentFeedbacks.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Recent Player Feedback</h3>
            <div className="space-y-4 max-h-64 overflow-y-auto">
              {feedbackStats.recentFeedbacks.map((fb) => (
                <div key={fb.id} className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center space-x-2">
                      <div className="text-yellow-400">
                        {'⭐'.repeat(fb.rating)}
                      </div>
                      <span className="text-sm text-gray-500">
                        {fb.difficulty && `• ${fb.difficulty} difficulty`}
                      </span>
                    </div>
                    <span className="text-xs text-gray-400">
                      {new Date(fb.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm mb-2">{fb.experience}</p>
                  {fb.suggestions && (
                    <p className="text-gray-600 text-xs italic">
                      💡 Suggestion: {fb.suggestions}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Difficulty Distribution */}
        {Object.keys(feedbackStats.difficultyDistribution).length > 0 && (
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-4">Popular Difficulty Levels</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(feedbackStats.difficultyDistribution).map(([difficulty, count]) => (
                <div key={difficulty} className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-xl font-bold text-gray-700">{count}</div>
                  <div className="text-sm text-gray-600 capitalize">{difficulty}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}