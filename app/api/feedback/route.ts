import { NextRequest, NextResponse } from 'next/server'

interface FeedbackData {
  rating: number
  difficulty: string
  experience: string
  suggestions: string
  timestamp: string
  userAgent?: string
  ip?: string
}

interface EmailResponse {
  success: boolean
  method?: string
  emailId?: string
  error?: string
}

export async function POST(request: NextRequest) {
  try {
    const feedbackData: FeedbackData = await request.json()
    
    // Get user info
    const userAgent = request.headers.get('user-agent') || 'Unknown'
    const ip = request.headers.get('x-forwarded-for') || 
               request.headers.get('x-real-ip') || 
               'Unknown'
    
    // Enhanced feedback data
    const enhancedFeedback = {
      ...feedbackData,
      userAgent,
      ip,
      submittedAt: new Date().toISOString()
    }

    // Try multiple email methods
    let emailResponse: EmailResponse = { success: false, error: 'No email service available' }
    
    // Method 1: Try Resend API
    try {
      emailResponse = await sendResendEmail(enhancedFeedback)
    } catch (error) {
      console.log('Resend failed, trying fallback methods')
      emailResponse = { success: false, error: 'Resend failed' }
    }
    
    // Method 2: Try direct SMTP if Resend fails
    if (!emailResponse.success) {
      try {
        emailResponse = await sendSMTPEmail(enhancedFeedback)
      } catch (error) {
        console.log('SMTP failed, trying webhook method')
        emailResponse = { success: false, error: 'SMTP failed' }
      }
    }
    
    // Method 3: Try webhook method if others fail
    if (!emailResponse.success) {
      try {
        emailResponse = await sendWebhookEmail(enhancedFeedback)
      } catch (error) {
        console.log('All email methods failed')
        emailResponse = { success: false, error: 'All methods failed' }
      }
    }

    return NextResponse.json({ 
      success: true, 
      message: 'Feedback received successfully!',
      emailSent: emailResponse.success,
      emailMethod: emailResponse.method || 'none'
    })

  } catch (error) {
    console.error('Feedback API error:', error)
    return NextResponse.json(
      { success: false, message: 'Failed to process feedback' },
      { status: 500 }
    )
  }
}

// Method 1: Resend API (Primary)
async function sendResendEmail(feedback: FeedbackData & { userAgent: string; ip: string; submittedAt: string }): Promise<EmailResponse> {
  try {
    const resendApiKey = process.env.RESEND_API_KEY
    
    if (!resendApiKey) {
      throw new Error('RESEND_API_KEY not configured')
    }

    const emailHtml = generateEmailHTML(feedback)
    const emailText = generateEmailText(feedback)

    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${resendApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'AI Tic-Tac-Toe <noreply@resend.dev>',
        to: ['squadmateai@gmail.com'],
        subject: `🎮 New Feedback: ${feedback.rating}⭐ - ${feedback.difficulty} difficulty`,
        html: emailHtml,
        text: emailText
      }),
    })

    if (!response.ok) {
      const errorData = await response.text()
      throw new Error(`Resend API error: ${response.status} - ${errorData}`)
    }

    const result = await response.json()
    console.log('Resend email sent successfully:', result.id)
    return { success: true, method: 'resend', emailId: result.id }

  } catch (error) {
    console.error('Resend email error:', error)
    throw error
  }
}

// Method 2: Direct SMTP (Fallback)
async function sendSMTPEmail(feedback: FeedbackData & { userAgent: string; ip: string; submittedAt: string }): Promise<EmailResponse> {
  try {
    // Using Gmail SMTP as fallback
    const gmailUser = process.env.GMAIL_USER
    const gmailPass = process.env.GMAIL_APP_PASSWORD
    
    if (!gmailUser || !gmailPass) {
      throw new Error('Gmail credentials not configured')
    }

    // Simple SMTP implementation using fetch to a serverless function
    const response = await fetch('https://api.emailjs.com/api/v1.0/email/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        service_id: 'gmail',
        template_id: 'feedback_template',
        user_id: process.env.EMAILJS_PUBLIC_KEY,
        accessToken: process.env.EMAILJS_PRIVATE_KEY,
        template_params: {
          to_email: 'squadmateai@gmail.com',
          from_name: 'AI Tic-Tac-Toe App',
          subject: `🎮 New Feedback: ${feedback.rating}⭐ - ${feedback.difficulty}`,
          message: generateEmailText(feedback)
        }
      }),
    })

    if (response.ok) {
      console.log('SMTP email sent successfully')
      return { success: true, method: 'smtp' }
    } else {
      throw new Error('SMTP send failed')
    }

  } catch (error) {
    console.error('SMTP email error:', error)
    throw error
  }
}

// Method 3: Webhook/Form submission (Last resort)
async function sendWebhookEmail(feedback: FeedbackData & { userAgent: string; ip: string; submittedAt: string }): Promise<EmailResponse> {
  try {
    // Using Formspree or similar service as last resort
    const formspreeEndpoint = process.env.FORMSPREE_ENDPOINT || 'https://formspree.io/f/xpwzgqvr'
    
    const response = await fetch(formspreeEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'squadmateai@gmail.com',
        subject: `🎮 AI Tic-Tac-Toe Feedback: ${feedback.rating}⭐`,
        message: generateEmailText(feedback),
        _replyto: 'noreply@tictactoe-ai.app',
        _subject: `🎮 New Feedback: ${feedback.rating}⭐ - ${feedback.difficulty} difficulty`
      }),
    })

    if (response.ok) {
      console.log('Webhook email sent successfully')
      return { success: true, method: 'webhook' }
    } else {
      throw new Error('Webhook send failed')
    }

  } catch (error) {
    console.error('Webhook email error:', error)
    throw error
  }
}

// Email template generators
function generateEmailHTML(feedback: FeedbackData & { userAgent: string; ip: string; submittedAt: string }) {
  return `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <h2 style="color: #2563eb; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">
        🎮 New AI Tic-Tac-Toe Feedback
      </h2>
      
      <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #374151; margin-top: 0;">Rating & Experience</h3>
        <p><strong>Rating:</strong> ${'⭐'.repeat(feedback.rating)} (${feedback.rating}/5)</p>
        <p><strong>Difficulty Played:</strong> <span style="text-transform: capitalize; background: #e0e7ff; padding: 2px 8px; border-radius: 4px;">${feedback.difficulty}</span></p>
        <p><strong>Experience:</strong></p>
        <blockquote style="background: white; padding: 15px; border-left: 4px solid #3b82f6; margin: 10px 0; font-style: italic;">
          ${feedback.experience}
        </blockquote>
        
        ${feedback.suggestions ? `
          <p><strong>Suggestions:</strong></p>
          <blockquote style="background: white; padding: 15px; border-left: 4px solid #10b981; margin: 10px 0; font-style: italic;">
            ${feedback.suggestions}
          </blockquote>
        ` : '<p><em>No suggestions provided</em></p>'}
      </div>

      <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; font-size: 12px; color: #64748b;">
        <h4 style="margin-top: 0; color: #475569;">📊 Technical Details</h4>
        <p><strong>Submitted:</strong> ${new Date(feedback.submittedAt).toLocaleString()}</p>
        <p><strong>User Agent:</strong> ${feedback.userAgent}</p>
        <p><strong>IP Address:</strong> ${feedback.ip}</p>
        <p><strong>Feedback ID:</strong> ${feedback.timestamp}</p>
      </div>

      <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
        <p>🤖 This feedback was automatically sent from the AI Tic-Tac-Toe Challenge app.</p>
        <p><a href="https://tictactoe-anwz1hzax-yangs-projects-33bbed0c.vercel.app" style="color: #2563eb; text-decoration: none;">🎮 Visit the app</a></p>
      </div>
    </div>
  `
}

function generateEmailText(feedback: FeedbackData & { userAgent: string; ip: string; submittedAt: string }) {
  return `
🎮 NEW AI TIC-TAC-TOE FEEDBACK

⭐ RATING: ${feedback.rating}/5 stars (${'⭐'.repeat(feedback.rating)})
🎯 DIFFICULTY: ${feedback.difficulty}

💬 PLAYER EXPERIENCE:
${feedback.experience}

${feedback.suggestions ? `💡 SUGGESTIONS:\n${feedback.suggestions}\n` : ''}

📊 TECHNICAL DETAILS:
- Submitted: ${new Date(feedback.submittedAt).toLocaleString()}
- User Agent: ${feedback.userAgent}
- IP Address: ${feedback.ip}
- Feedback ID: ${feedback.timestamp}

🤖 Sent automatically from AI Tic-Tac-Toe Challenge
🌐 Visit: https://tictactoe-anwz1hzax-yangs-projects-33bbed0c.vercel.app
  `.trim()
}

