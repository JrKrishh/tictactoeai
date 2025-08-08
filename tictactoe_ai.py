import random
import math
import json
import numpy as np
import csv
import time
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass

@dataclass
class GameRecord:
    """Record of a single game for training data"""
    game_id: int
    player_x_strategy: str
    player_o_strategy: str
    moves: List[Tuple[str, int, str]]  # (board_state, move, player)
    winner: str
    game_length: int
    timestamp: str
    
@dataclass
class TrainingDataset:
    """Collection of game records for training"""
    games: List[GameRecord]
    total_games: int
    strategy_matchups: Dict[str, int]
    win_rates: Dict[str, Dict[str, float]]

class GameplayDataCollector:
    """Collects and manages training data from AI vs AI games"""
    
    def __init__(self):
        self.games_data = []
        self.current_game_id = 0
        
    def record_game(self, game_record: GameRecord):
        """Add a game record to the dataset"""
        self.games_data.append(game_record)
        
    def export_to_csv(self, filename: str = "training_data.csv"):
        """Export training data to CSV format"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['game_id', 'player_x_strategy', 'player_o_strategy', 
                         'winner', 'game_length', 'timestamp', 'moves_sequence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for game in self.games_data:
                moves_str = ';'.join([f"{state},{move},{player}" for state, move, player in game.moves])
                writer.writerow({
                    'game_id': game.game_id,
                    'player_x_strategy': game.player_x_strategy,
                    'player_o_strategy': game.player_o_strategy,
                    'winner': game.winner,
                    'game_length': game.game_length,
                    'timestamp': game.timestamp,
                    'moves_sequence': moves_str
                })
        print(f"Training data exported to {filename}")
        
    def export_to_json(self, filename: str = "training_data.json"):
        """Export training data to JSON format"""
        data = {
            'metadata': {
                'total_games': len(self.games_data),
                'export_timestamp': datetime.now().isoformat(),
                'strategies_used': list(set([g.player_x_strategy for g in self.games_data] + 
                                          [g.player_o_strategy for g in self.games_data]))
            },
            'games': [
                {
                    'game_id': game.game_id,
                    'player_x_strategy': game.player_x_strategy,
                    'player_o_strategy': game.player_o_strategy,
                    'moves': [{'board_state': state, 'move': move, 'player': player} 
                             for state, move, player in game.moves],
                    'winner': game.winner,
                    'game_length': game.game_length,
                    'timestamp': game.timestamp
                } for game in self.games_data
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Training data exported to {filename}")
        
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the collected data"""
        if not self.games_data:
            return {"error": "No games recorded"}
            
        stats = {
            'total_games': len(self.games_data),
            'strategy_usage': defaultdict(int),
            'win_rates': defaultdict(lambda: {'wins': 0, 'total': 0}),
            'matchup_results': defaultdict(lambda: {'X_wins': 0, 'O_wins': 0, 'ties': 0}),
            'average_game_length': 0,
            'game_length_distribution': defaultdict(int)
        }
        
        total_length = 0
        for game in self.games_data:
            # Strategy usage
            stats['strategy_usage'][game.player_x_strategy] += 1
            stats['strategy_usage'][game.player_o_strategy] += 1
            
            # Win rates
            if game.winner != 'Tie':
                if game.winner == 'X':
                    stats['win_rates'][game.player_x_strategy]['wins'] += 1
                else:
                    stats['win_rates'][game.player_o_strategy]['wins'] += 1
            
            stats['win_rates'][game.player_x_strategy]['total'] += 1
            stats['win_rates'][game.player_o_strategy]['total'] += 1
            
            # Matchup results
            matchup = f"{game.player_x_strategy}_vs_{game.player_o_strategy}"
            if game.winner == 'X':
                stats['matchup_results'][matchup]['X_wins'] += 1
            elif game.winner == 'O':
                stats['matchup_results'][matchup]['O_wins'] += 1
            else:
                stats['matchup_results'][matchup]['ties'] += 1
                
            # Game length
            total_length += game.game_length
            stats['game_length_distribution'][game.game_length] += 1
            
        stats['average_game_length'] = total_length / len(self.games_data)
        
        # Calculate win rate percentages
        for strategy in stats['win_rates']:
            if stats['win_rates'][strategy]['total'] > 0:
                win_rate = stats['win_rates'][strategy]['wins'] / stats['win_rates'][strategy]['total']
                stats['win_rates'][strategy]['percentage'] = win_rate * 100
                
        return dict(stats)

class Strategy(Enum):
    MINIMAX = "minimax"
    Q_LEARNING = "q_learning"
    RANDOM = "random"
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    HYBRID = "hybrid"

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.game_history = []
        
    def get_state_key(self, board: List[str]) -> str:
        """Convert board state to string key"""
        return ''.join(board)
    
    def get_q_value(self, state: str, action: int) -> float:
        """Get Q-value for state-action pair"""
        return self.q_table[state][action]
    
    def update_q_value(self, state: str, action: int, reward: float, next_state: str, available_actions: List[int]):
        """Update Q-value using Q-learning formula"""
        current_q = self.get_q_value(state, action)
        
        if available_actions:
            max_next_q = max([self.get_q_value(next_state, a) for a in available_actions])
        else:
            max_next_q = 0
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def choose_action(self, state: str, available_actions: List[int], training: bool = True) -> int:
        """Choose action using epsilon-greedy policy"""
        if training and random.random() < self.epsilon:
            return random.choice(available_actions)
        
        q_values = {action: self.get_q_value(state, action) for action in available_actions}
        return max(q_values, key=q_values.get)
    
    def save_q_table(self, filename: str):
        """Save Q-table to file"""
        q_dict = {state: dict(actions) for state, actions in self.q_table.items()}
        with open(filename, 'w') as f:
            json.dump(q_dict, f, indent=2)
    
    def load_q_table(self, filename: str):
        """Load Q-table from file"""
        try:
            with open(filename, 'r') as f:
                q_dict = json.load(f)
                self.q_table = defaultdict(lambda: defaultdict(float))
                for state, actions in q_dict.items():
                    for action, value in actions.items():
                        self.q_table[state][int(action)] = value
        except FileNotFoundError:
            print(f"Q-table file {filename} not found. Starting with empty Q-table.")

class TicTacToeAI:
    def __init__(self, strategy_x: Strategy = Strategy.MINIMAX, strategy_o: Strategy = Strategy.MINIMAX):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.strategy_x = strategy_x
        self.strategy_o = strategy_o
        self.q_agent_x = QLearningAgent()
        self.q_agent_o = QLearningAgent()
        self.game_states = []  # Track states for learning
        self.data_collector = GameplayDataCollector()  # For training data collection
        self.current_game_moves = []  # Track moves for current game
        
    def reset_board(self):
        """Reset the game board"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
    
    def print_board(self):
        """Print the current board state"""
        print("\n" + "-" * 13)
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            print(f"| {row[0]} | {row[1]} | {row[2]} |")
            print("-" * 13)
    
    def is_valid_move(self, position: int) -> bool:
        """Check if a move is valid"""
        return 0 <= position < 9 and self.board[position] == ' '
    
    def make_move(self, position: int, player: str) -> bool:
        """Make a move on the board"""
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False
    
    def check_winner(self) -> Optional[str]:
        """Check if there's a winner"""
        # Winning combinations
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in wins:
            if (self.board[combo[0]] == self.board[combo[1]] == 
                self.board[combo[2]] != ' '):
                return self.board[combo[0]]
        
        # Check for tie
        if ' ' not in self.board:
            return 'Tie'
        
        return None
    
    def get_available_moves(self) -> List[int]:
        """Get list of available moves"""
        return [i for i in range(9) if self.board[i] == ' ']
    
    def minimax(self, depth: int, is_maximizing: bool, alpha: float = -math.inf, beta: float = math.inf) -> int:
        """Minimax algorithm with alpha-beta pruning"""
        winner = self.check_winner()
        
        if winner == 'X':
            return 10 - depth
        elif winner == 'O':
            return depth - 10
        elif winner == 'Tie':
            return 0
        
        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_available_moves():
                self.board[move] = 'X'
                eval_score = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = ' '
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_available_moves():
                self.board[move] = 'O'
                eval_score = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = ' '
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self, player: str) -> int:
        """Get the best move using minimax"""
        best_score = -math.inf if player == 'X' else math.inf
        best_move = -1
        
        for move in self.get_available_moves():
            self.board[move] = player
            score = self.minimax(0, player == 'O')
            self.board[move] = ' '
            
            if player == 'X' and score > best_score:
                best_score = score
                best_move = move
            elif player == 'O' and score < best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_random_move(self) -> int:
        """Get a random valid move"""
        return random.choice(self.get_available_moves())
    
    def get_aggressive_move(self, player: str) -> int:
        """Aggressive strategy: prioritize winning moves, then center, then corners"""
        available = self.get_available_moves()
        
        # First, check for winning moves
        for move in available:
            self.board[move] = player
            if self.check_winner() == player:
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        
        # Then prioritize center
        if 4 in available:
            return 4
        
        # Then corners
        corners = [0, 2, 6, 8]
        corner_moves = [m for m in available if m in corners]
        if corner_moves:
            return random.choice(corner_moves)
        
        # Finally, any available move
        return random.choice(available)
    
    def get_defensive_move(self, player: str) -> int:
        """Defensive strategy: block opponent wins, then play safe"""
        available = self.get_available_moves()
        opponent = 'O' if player == 'X' else 'X'
        
        # First, check for blocking moves
        for move in available:
            self.board[move] = opponent
            if self.check_winner() == opponent:
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        
        # Then check for our winning moves
        for move in available:
            self.board[move] = player
            if self.check_winner() == player:
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        
        # Play center if available
        if 4 in available:
            return 4
        
        # Play edges (safer than corners)
        edges = [1, 3, 5, 7]
        edge_moves = [m for m in available if m in edges]
        if edge_moves:
            return random.choice(edge_moves)
        
        return random.choice(available)
    
    def get_hybrid_move(self, player: str) -> int:
        """Hybrid strategy: mix of minimax and heuristics"""
        available = self.get_available_moves()
        
        # Early game: use heuristics
        if len(available) > 6:
            return self.get_aggressive_move(player)
        # Late game: use minimax
        else:
            return self.get_best_move(player)
    
    def get_move_by_strategy(self, player: str, strategy: Strategy, training: bool = False) -> int:
        """Get move based on specified strategy"""
        if strategy == Strategy.MINIMAX:
            return self.get_best_move(player)
        elif strategy == Strategy.Q_LEARNING:
            agent = self.q_agent_x if player == 'X' else self.q_agent_o
            state = agent.get_state_key(self.board)
            return agent.choose_action(state, self.get_available_moves(), training)
        elif strategy == Strategy.RANDOM:
            return self.get_random_move()
        elif strategy == Strategy.AGGRESSIVE:
            return self.get_aggressive_move(player)
        elif strategy == Strategy.DEFENSIVE:
            return self.get_defensive_move(player)
        elif strategy == Strategy.HYBRID:
            return self.get_hybrid_move(player)
        else:
            return self.get_best_move(player)
    
    def update_q_learning(self, winner: str):
        """Update Q-learning agents based on game outcome"""
        # Define rewards
        rewards = {'X': 1, 'O': -1, 'Tie': 0}
        
        # Update Q-values for both agents
        for i, (state, action, player) in enumerate(self.game_states):
            if player == 'X':
                agent = self.q_agent_x
                reward = rewards.get(winner, 0) if winner == 'X' else (0 if winner == 'Tie' else -1)
            else:
                agent = self.q_agent_o
                reward = rewards.get(winner, 0) if winner == 'O' else (0 if winner == 'Tie' else -1)
            
            # Get next state
            if i + 1 < len(self.game_states):
                next_state = self.game_states[i + 1][0]
                # Find available actions in next state
                next_board = list(next_state)
                next_available = [j for j in range(9) if next_board[j] == ' ']
            else:
                next_state = state
                next_available = []
            
            agent.update_q_value(state, action, reward, next_state, next_available)
    
    def play_self_game(self, show_board: bool = False, training: bool = False, collect_data: bool = False) -> str:
        """Play a complete game between two AI agents"""
        self.reset_board()
        self.game_states = []
        self.current_game_moves = []
        game_start_time = datetime.now()
        
        while True:
            if show_board:
                self.print_board()
                strategy = self.strategy_x if self.current_player == 'X' else self.strategy_o
                print(f"Player {self.current_player}'s turn ({strategy.value})")
            
            # Record current board state
            current_state = ''.join(self.board)
            
            # Record state for Q-learning
            if training and (self.strategy_x == Strategy.Q_LEARNING or self.strategy_o == Strategy.Q_LEARNING):
                state = current_state
            
            # Get move based on player's strategy
            strategy = self.strategy_x if self.current_player == 'X' else self.strategy_o
            move = self.get_move_by_strategy(self.current_player, strategy, training)
            
            # Record move for training data collection
            if collect_data:
                self.current_game_moves.append((current_state, move, self.current_player))
            
            # Record state-action pair for learning
            if training and (self.strategy_x == Strategy.Q_LEARNING or self.strategy_o == Strategy.Q_LEARNING):
                self.game_states.append((state, move, self.current_player))
            
            self.make_move(move, self.current_player)
            
            # Check for game end
            winner = self.check_winner()
            if winner:
                if show_board:
                    self.print_board()
                    print(f"Game Over! Winner: {winner}")
                
                # Update Q-learning if training
                if training and (self.strategy_x == Strategy.Q_LEARNING or self.strategy_o == Strategy.Q_LEARNING):
                    self.update_q_learning(winner)
                
                # Collect training data
                if collect_data:
                    game_record = GameRecord(
                        game_id=self.data_collector.current_game_id,
                        player_x_strategy=self.strategy_x.value,
                        player_o_strategy=self.strategy_o.value,
                        moves=self.current_game_moves,
                        winner=winner,
                        game_length=len(self.current_game_moves),
                        timestamp=game_start_time.isoformat()
                    )
                    self.data_collector.record_game(game_record)
                    self.data_collector.current_game_id += 1
                
                return winner
            
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def run_self_play_tournament(self, num_games: int = 100, training: bool = False) -> dict:
        """Run multiple self-play games and collect statistics"""
        results = {'X': 0, 'O': 0, 'Tie': 0}
        
        print(f"Running {num_games} self-play games...")
        print(f"X Strategy: {self.strategy_x.value}, O Strategy: {self.strategy_o.value}")
        if training:
            print("Training mode: Q-learning agents will learn from games")
        
        for i in range(num_games):
            if (i + 1) % 10 == 0:
                print(f"Completed {i + 1} games")
            
            winner = self.play_self_game(training=training)
            results[winner] += 1
        
        print("\n=== Tournament Results ===")
        print(f"X wins: {results['X']} ({results['X']/num_games*100:.1f}%)")
        print(f"O wins: {results['O']} ({results['O']/num_games*100:.1f}%)")
        print(f"Ties: {results['Tie']} ({results['Tie']/num_games*100:.1f}%)")
        
        return results
    
    def train_q_learning_agent(self, episodes: int = 1000, opponent_strategy: Strategy = Strategy.RANDOM):
        """Train Q-learning agent against different opponents"""
        print(f"Training Q-learning agent for {episodes} episodes against {opponent_strategy.value}")
        
        # Set up training configuration
        original_x = self.strategy_x
        original_o = self.strategy_o
        
        self.strategy_x = Strategy.Q_LEARNING
        self.strategy_o = opponent_strategy
        
        # Training phase
        results = {'X': 0, 'O': 0, 'Tie': 0}
        for i in range(episodes):
            if (i + 1) % 100 == 0:
                print(f"Training episode {i + 1}/{episodes}")
            
            winner = self.play_self_game(training=True)
            results[winner] += 1
        
        print(f"\nTraining completed!")
        print(f"Training results - X: {results['X']}, O: {results['O']}, Ties: {results['Tie']}")
        
        # Restore original strategies
        self.strategy_x = original_x
        self.strategy_o = original_o
    
    def evaluate_strategies(self, strategies: List[Strategy], num_games: int = 50):
        """Evaluate different strategies against each other"""
        print("=== Strategy Evaluation ===")
        results = {}
        
        for i, strat_x in enumerate(strategies):
            for j, strat_o in enumerate(strategies):
                if i <= j:  # Avoid duplicate matchups
                    print(f"\n{strat_x.value} vs {strat_o.value}")
                    
                    # Set strategies
                    self.strategy_x = strat_x
                    self.strategy_o = strat_o
                    
                    # Run games
                    game_results = self.run_self_play_tournament(num_games)
                    results[f"{strat_x.value}_vs_{strat_o.value}"] = game_results
        
        return results
    
    def save_q_tables(self, prefix: str = "q_table"):
        """Save Q-tables for both agents"""
        self.q_agent_x.save_q_table(f"{prefix}_x.json")
        self.q_agent_o.save_q_table(f"{prefix}_o.json")
        print(f"Q-tables saved as {prefix}_x.json and {prefix}_o.json")
    
    def load_q_tables(self, prefix: str = "q_table"):
        """Load Q-tables for both agents"""
        self.q_agent_x.load_q_table(f"{prefix}_x.json")
        self.q_agent_o.load_q_table(f"{prefix}_o.json")
        print(f"Q-tables loaded from {prefix}_x.json and {prefix}_o.json")
    
    def play_interactive_game(self):
        """Play an interactive game against the AI"""
        print("=== Interactive Game vs AI ===")
        print("You are X, AI is O")
        print("Enter positions 0-8 (top-left to bottom-right)")
        
        self.reset_board()
        self.strategy_o = Strategy.MINIMAX  # AI uses minimax
        
        while True:
            self.print_board()
            
            if self.current_player == 'X':
                # Human player
                try:
                    move = int(input("Your move (0-8): "))
                    if not self.is_valid_move(move):
                        print("Invalid move! Try again.")
                        continue
                except ValueError:
                    print("Please enter a number 0-8")
                    continue
            else:
                # AI player
                move = self.get_move_by_strategy('O', self.strategy_o)
                print(f"AI plays position {move}")
            
            self.make_move(move, self.current_player)
            
            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == 'X':
                    print("Congratulations! You won!")
                elif winner == 'O':
                    print("AI wins! Better luck next time.")
                else:
                    print("It's a tie!")
                break
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def generate_training_data(self, strategy_pairs: List[Tuple[Strategy, Strategy]], 
                             games_per_pair: int = 100, export_format: str = "both") -> Dict:
        """Generate comprehensive training data from AI vs AI gameplay"""
        print("🎯 Generating Training Data from AI vs AI Gameplay")
        print("=" * 60)
        
        total_games = len(strategy_pairs) * games_per_pair
        print(f"Total games to play: {total_games}")
        print(f"Strategy pairs: {len(strategy_pairs)}")
        
        # Reset data collector
        self.data_collector = GameplayDataCollector()
        
        start_time = time.time()
        games_played = 0
        
        for i, (strat_x, strat_o) in enumerate(strategy_pairs):
            print(f"\n📊 Matchup {i+1}/{len(strategy_pairs)}: {strat_x.value} vs {strat_o.value}")
            
            # Set strategies
            self.strategy_x = strat_x
            self.strategy_o = strat_o
            
            # Play games and collect data
            for j in range(games_per_pair):
                self.play_self_game(collect_data=True)
                games_played += 1
                
                if games_played % 50 == 0:
                    elapsed = time.time() - start_time
                    print(f"  Progress: {games_played}/{total_games} games ({games_played/total_games*100:.1f}%) - {elapsed:.1f}s")
        
        # Generate statistics
        stats = self.data_collector.get_statistics()
        
        # Export data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if export_format in ["csv", "both"]:
            self.data_collector.export_to_csv(f"training_data_{timestamp}.csv")
        if export_format in ["json", "both"]:
            self.data_collector.export_to_json(f"training_data_{timestamp}.json")
        
        print(f"\n✅ Training data generation completed!")
        print(f"Total time: {time.time() - start_time:.1f} seconds")
        print(f"Games per second: {games_played/(time.time() - start_time):.1f}")
        
        return stats
    
    def run_comprehensive_ai_tournament(self, num_games_per_matchup: int = 50) -> Dict:
        """Run a comprehensive tournament between all AI strategies"""
        print("🏆 Comprehensive AI vs AI Tournament")
        print("=" * 60)
        
        all_strategies = list(Strategy)
        strategy_pairs = []
        
        # Generate all unique strategy pairs (including self-play)
        for i, strat_x in enumerate(all_strategies):
            for j, strat_o in enumerate(all_strategies):
                if i <= j:  # Include self-play and avoid duplicates
                    strategy_pairs.append((strat_x, strat_o))
        
        print(f"Tournament includes {len(strategy_pairs)} unique matchups")
        print(f"Each matchup plays {num_games_per_matchup} games")
        
        # Generate training data from tournament
        stats = self.generate_training_data(strategy_pairs, num_games_per_matchup)
        
        # Print comprehensive results
        self.print_tournament_analysis(stats)
        
        return stats
    
    def print_tournament_analysis(self, stats: Dict):
        """Print detailed analysis of tournament results"""
        print("\n" + "=" * 60)
        print("📈 TOURNAMENT ANALYSIS")
        print("=" * 60)
        
        print(f"\n🎮 Overall Statistics:")
        print(f"  Total games played: {stats['total_games']}")
        print(f"  Average game length: {stats['average_game_length']:.1f} moves")
        
        print(f"\n🏅 Strategy Performance:")
        for strategy, data in stats['win_rates'].items():
            if data['total'] > 0:
                print(f"  {strategy:12} - Win Rate: {data['percentage']:.1f}% ({data['wins']}/{data['total']})")
        
        print(f"\n⚔️  Head-to-Head Results:")
        for matchup, results in stats['matchup_results'].items():
            total = results['X_wins'] + results['O_wins'] + results['ties']
            if total > 0:
                x_rate = results['X_wins'] / total * 100
                o_rate = results['O_wins'] / total * 100
                tie_rate = results['ties'] / total * 100
                print(f"  {matchup:25} - X: {x_rate:4.1f}% | O: {o_rate:4.1f}% | Tie: {tie_rate:4.1f}%")
        
        print(f"\n📊 Game Length Distribution:")
        for length, count in sorted(stats['game_length_distribution'].items()):
            percentage = count / stats['total_games'] * 100
            print(f"  {length} moves: {count:4} games ({percentage:4.1f}%)")
    
    def create_custom_training_dataset(self, focus_strategies: List[Strategy], 
                                     games_per_strategy: int = 200) -> Dict:
        """Create a focused training dataset with specific strategies"""
        print(f"🎯 Creating Custom Training Dataset")
        print(f"Focus strategies: {[s.value for s in focus_strategies]}")
        
        strategy_pairs = []
        
        # Create pairs focusing on the specified strategies
        for strat in focus_strategies:
            # Self-play
            strategy_pairs.append((strat, strat))
            
            # Against other focus strategies
            for other_strat in focus_strategies:
                if strat != other_strat:
                    strategy_pairs.append((strat, other_strat))
            
            # Against random (for learning baseline)
            if Strategy.RANDOM not in focus_strategies:
                strategy_pairs.append((strat, Strategy.RANDOM))
                strategy_pairs.append((Strategy.RANDOM, strat))
        
        # Remove duplicates while preserving order
        unique_pairs = []
        seen = set()
        for pair in strategy_pairs:
            if pair not in seen and (pair[1], pair[0]) not in seen:
                unique_pairs.append(pair)
                seen.add(pair)
        
        return self.generate_training_data(unique_pairs, games_per_strategy)
    
    def analyze_gameplay_patterns(self) -> Dict:
        """Analyze patterns in the collected gameplay data"""
        if not self.data_collector.games_data:
            return {"error": "No gameplay data available"}
        
        print("🔍 Analyzing Gameplay Patterns")
        print("=" * 40)
        
        patterns = {
            'opening_moves': defaultdict(int),
            'winning_sequences': defaultdict(int),
            'strategy_effectiveness': defaultdict(lambda: {'wins': 0, 'games': 0}),
            'common_endgames': defaultdict(int)
        }
        
        for game in self.data_collector.games_data:
            # Opening move analysis
            if game.moves:
                first_move = game.moves[0][1]  # First move position
                patterns['opening_moves'][first_move] += 1
            
            # Strategy effectiveness
            x_strat = game.player_x_strategy
            o_strat = game.player_o_strategy
            
            patterns['strategy_effectiveness'][x_strat]['games'] += 1
            patterns['strategy_effectiveness'][o_strat]['games'] += 1
            
            if game.winner == 'X':
                patterns['strategy_effectiveness'][x_strat]['wins'] += 1
            elif game.winner == 'O':
                patterns['strategy_effectiveness'][o_strat]['wins'] += 1
            
            # Game length patterns
            patterns['common_endgames'][game.game_length] += 1
        
        # Calculate win rates
        for strategy in patterns['strategy_effectiveness']:
            data = patterns['strategy_effectiveness'][strategy]
            if data['games'] > 0:
                data['win_rate'] = data['wins'] / data['games'] * 100
        
        # Print analysis
        print(f"\n📍 Most Popular Opening Moves:")
        for move, count in sorted(patterns['opening_moves'].items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = count / len(self.data_collector.games_data) * 100
            print(f"  Position {move}: {count} times ({percentage:.1f}%)")
        
        print(f"\n🎯 Strategy Win Rates:")
        for strategy, data in patterns['strategy_effectiveness'].items():
            if data['games'] > 0:
                print(f"  {strategy:12}: {data['win_rate']:5.1f}% ({data['wins']}/{data['games']})")
        
        return dict(patterns)

if __name__ == "__main__":
    print("🎮 AI vs AI Tic-Tac-Toe Gameplay & Training Data Generator")
    print("=" * 70)
    
    # Demo 1: Quick AI vs AI gameplay showcase
    print("\n1. 🎯 AI vs AI Gameplay Showcase")
    print("-" * 40)
    
    ai = TicTacToeAI(Strategy.MINIMAX, Strategy.AGGRESSIVE)
    print("Sample game: Minimax vs Aggressive")
    ai.play_self_game(show_board=True)
    
    # Demo 2: Training data generation
    print("\n" + "="*70)
    print("2. 📊 Training Data Generation Demo")
    print("-" * 40)
    
    # Create focused training dataset
    training_ai = TicTacToeAI()
    focus_strategies = [Strategy.MINIMAX, Strategy.AGGRESSIVE, Strategy.DEFENSIVE]
    
    print("Generating training data with focused strategies...")
    stats = training_ai.create_custom_training_dataset(focus_strategies, games_per_strategy=30)
    
    # Demo 3: Comprehensive tournament
    print("\n" + "="*70)
    print("3. 🏆 Mini Tournament (All Strategies)")
    print("-" * 40)
    
    tournament_ai = TicTacToeAI()
    tournament_stats = tournament_ai.run_comprehensive_ai_tournament(num_games_per_matchup=20)
    
    # Demo 4: Gameplay pattern analysis
    print("\n" + "="*70)
    print("4. 🔍 Gameplay Pattern Analysis")
    print("-" * 40)
    
    patterns = tournament_ai.analyze_gameplay_patterns()
    
    # Demo 5: Q-Learning with data collection
    print("\n" + "="*70)
    print("5. 🧠 Q-Learning Training with Data Collection")
    print("-" * 40)
    
    learning_ai = TicTacToeAI()
    print("Training Q-learning agent...")
    learning_ai.train_q_learning_agent(episodes=200, opponent_strategy=Strategy.RANDOM)
    
    # Test the trained agent and collect data
    print("\nTesting trained agent vs different strategies...")
    test_pairs = [
        (Strategy.Q_LEARNING, Strategy.MINIMAX),
        (Strategy.Q_LEARNING, Strategy.AGGRESSIVE),
        (Strategy.Q_LEARNING, Strategy.DEFENSIVE)
    ]
    
    learning_stats = learning_ai.generate_training_data(test_pairs, games_per_pair=20, export_format="json")
    
    # Demo 6: Interactive options
    print("\n" + "="*70)
    print("6. 🎮 Available Interactive Features")
    print("-" * 40)
    print("Run these commands for interactive gameplay:")
    print("  ai = TicTacToeAI()")
    print("  ai.play_interactive_game()  # Play against AI")
    print("  ai.run_comprehensive_ai_tournament(100)  # Full tournament")
    print("  ai.generate_training_data(strategy_pairs, 500)  # Large dataset")
    print("  ai.analyze_gameplay_patterns()  # Pattern analysis")
    
    # Summary
    print("\n" + "="*70)
    print("✅ AI vs AI Gameplay System Ready!")
    print("=" * 70)
    print("\n🎯 Key Features Demonstrated:")
    print("  ✓ Multiple AI strategies (6 different approaches)")
    print("  ✓ Q-learning with reinforcement learning")
    print("  ✓ Comprehensive training data collection")
    print("  ✓ CSV and JSON export formats")
    print("  ✓ Statistical analysis and pattern recognition")
    print("  ✓ Tournament system with all strategy matchups")
    print("  ✓ Real-time gameplay visualization")
    
    print("\n📁 Generated Files:")
    print("  - training_data_[timestamp].csv")
    print("  - training_data_[timestamp].json")
    print("  - q_table_x.json / q_table_o.json (if Q-learning used)")
    
    print("\n🚀 Ready for Production Use:")
    print("  - Scale up games_per_pair for larger datasets")
    print("  - Use different strategy combinations")
    print("  - Export data for machine learning pipelines")
    print("  - Analyze patterns for strategy optimization")