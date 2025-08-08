# 🤝 Contributing to AI Tic-Tac-Toe Challenge

Thank you for your interest in contributing to the AI Tic-Tac-Toe Challenge! This document provides guidelines and information for contributors.

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide browser/device information
- Add screenshots if helpful

### 💡 Feature Requests
- Use GitHub Discussions for feature ideas
- Explain the use case and benefits
- Consider implementation complexity
- Check existing issues first

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Add tests for new features
- Update documentation

### 📖 Documentation
- Improve README clarity
- Add code comments
- Create tutorials or guides
- Fix typos and grammar

## 🚀 Development Setup

### Prerequisites
```bash
# Required
Node.js 18+
Python 3.8+
Git

# Optional (for email testing)
Resend API key
Formspree account
```

### Local Development
```bash
# 1. Fork and clone
git clone https://github.com/yourusername/ai-tictactoe-challenge.git
cd ai-tictactoe-challenge

# 2. Install dependencies
npm install

# 3. Set up environment
cp .env.example .env.local
# Edit .env.local with your API keys

# 4. Start development server
npm run dev

# 5. Open browser
# Visit http://localhost:3000
```

## 📝 Coding Standards

### TypeScript/React
```typescript
// Use TypeScript for type safety
interface GameState {
  board: Player[]
  currentPlayer: Player
  status: GameStatus
}

// Use functional components with hooks
const GameComponent: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>(initialState)
  
  return <div>Game content</div>
}

// Use descriptive variable names
const isPlayerTurn = currentPlayer === 'X'
const availableMoves = getEmptyPositions(board)
```

### CSS/Styling
```css
/* Use Tailwind CSS classes */
<button className="btn-primary hover:bg-blue-700 transition-colors">
  Click me
</button>

/* Custom styles in globals.css */
.game-cell {
  @apply w-20 h-20 border-2 border-gray-300 flex items-center justify-center;
}
```

### Python (AI/Training)
```python
# Follow PEP 8 style guide
def generate_training_data(strategy_pairs: List[Tuple], 
                          games_per_pair: int = 1000) -> Dict:
    """Generate training data from AI vs AI games.
    
    Args:
        strategy_pairs: List of (strategy_x, strategy_o) tuples
        games_per_pair: Number of games per strategy combination
        
    Returns:
        Dictionary containing game statistics and data
    """
    pass

# Use type hints
from typing import List, Dict, Optional, Tuple

# Use descriptive names
def calculate_win_rate(wins: int, total_games: int) -> float:
    return wins / total_games if total_games > 0 else 0.0
```

## 🧪 Testing Guidelines

### Frontend Testing
```bash
# Run type checking
npm run type-check

# Run linting
npm run lint

# Build for production
npm run build

# Test locally
npm run start
```

### Manual Testing Checklist
- [ ] All difficulty levels work correctly
- [ ] AI-first toggle functions properly
- [ ] Feedback form submits successfully
- [ ] Email notifications are sent
- [ ] Game statistics update correctly
- [ ] Responsive design on mobile/tablet
- [ ] Accessibility features work
- [ ] Performance is acceptable

### AI Testing
```python
# Test AI strategies
python -c "
from tictactoe_ai import TicTacToeAI, Strategy
ai = TicTacToeAI(Strategy.EXPERT, Strategy.RANDOM)
results = ai.run_self_play_tournament(100)
print(f'Expert win rate: {results[\"X\"]/100*100:.1f}%')
"

# Test training data generation
python large_scale_training.py
```

## 📋 Pull Request Process

### Before Submitting
1. **Test thoroughly** on multiple browsers
2. **Update documentation** if needed
3. **Add/update tests** for new features
4. **Follow commit message format**
5. **Rebase on latest main** branch

### Commit Message Format
```
type(scope): brief description

Detailed explanation of changes (if needed)

- List specific changes
- Include breaking changes
- Reference issues: Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ai): add Monte Carlo Tree Search strategy

Implement MCTS algorithm for advanced AI difficulty level.
Includes tree expansion, simulation, and backpropagation.

- Add MCTSStrategy class
- Integrate with existing AI system
- Update difficulty selection UI
- Add performance benchmarks

Fixes #45
```

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Manual testing completed
- [ ] All builds pass
- [ ] Cross-browser testing done

## Screenshots (if applicable)
Add screenshots of UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🎨 Design Guidelines

### UI/UX Principles
- **Accessibility first**: WCAG 2.1 AA compliance
- **Mobile responsive**: Works on all screen sizes
- **Performance**: Fast loading and smooth animations
- **Intuitive**: Clear navigation and feedback
- **Consistent**: Follow established patterns

### Color Scheme
```css
/* Primary colors */
--blue-500: #3b82f6;    /* Primary actions */
--green-500: #10b981;   /* Success states */
--red-500: #ef4444;     /* Errors/AI moves */
--yellow-500: #f59e0b;  /* Warnings/ties */

/* Neutral colors */
--gray-50: #f9fafb;     /* Backgrounds */
--gray-600: #4b5563;    /* Text */
--gray-800: #1f2937;    /* Headings */
```

### Typography
- **Headings**: Inter font, bold weights
- **Body text**: Inter font, regular weight
- **Code**: Monospace font for technical content
- **Sizes**: Responsive scaling with Tailwind

## 🔧 Architecture Guidelines

### Component Structure
```
components/
├── TicTacToeGame.tsx     # Main game logic
├── FeedbackSystem.tsx    # Feedback collection
├── GameBoard.tsx         # Board display
├── GameStats.tsx         # Statistics display
└── common/
    ├── Button.tsx        # Reusable button
    └── Modal.tsx         # Modal component
```

### State Management
- Use React hooks for local state
- Context API for global state
- LocalStorage for persistence
- No external state library needed

### API Design
```typescript
// RESTful endpoints
POST /api/feedback        # Submit feedback
GET  /api/stats          # Get game statistics
POST /api/training       # Generate training data

// Response format
interface APIResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}
```

## 🚀 Deployment

### Vercel Deployment
- Automatic deployment on push to main
- Preview deployments for pull requests
- Environment variables in Vercel dashboard
- Custom domain configuration available

### Environment Variables
```bash
# Required for email functionality
RESEND_API_KEY=your_resend_key

# Optional fallbacks
FORMSPREE_ENDPOINT=your_formspree_url
GMAIL_USER=your_gmail
GMAIL_APP_PASSWORD=your_app_password
```

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: Use in-app feedback for direct contact
- **Documentation**: Check README and setup guides

### Response Times
- **Bug reports**: 1-2 days
- **Feature requests**: 1 week
- **Pull requests**: 2-3 days
- **Questions**: 1-2 days

## 🏆 Recognition

### Contributors
All contributors will be:
- Listed in the README
- Credited in release notes
- Invited to join the maintainers team (for significant contributions)

### Contribution Types
- 🐛 **Bug fixes**: Help improve stability
- ✨ **Features**: Add new functionality
- 📖 **Documentation**: Improve clarity
- 🎨 **Design**: Enhance user experience
- 🧪 **Testing**: Increase reliability
- 🔧 **Infrastructure**: Improve development

## 📜 Code of Conduct

### Our Standards
- **Be respectful** and inclusive
- **Be constructive** in feedback
- **Be patient** with newcomers
- **Be collaborative** in discussions

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Spam or off-topic content

### Enforcement
- Issues will be addressed promptly
- Violations may result in temporary or permanent bans
- Contact maintainers for serious issues

---

## 🎉 Thank You!

Your contributions make this project better for everyone. Whether you're fixing a typo, adding a feature, or reporting a bug, every contribution is valuable and appreciated!

**Happy coding! 🚀**