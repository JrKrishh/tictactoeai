#!/usr/bin/env python3
"""
Interactive Q-Learning Agent Test
=================================
Watch the Q-learning agent make decisions in real-time
"""

from tictactoe_ai import TicTacToeAI, Strategy
import time

def interactive_q_learning_demo():
    print("🎮 INTERACTIVE Q-LEARNING DEMONSTRATION")
    print("=" * 50)
    
    # Train the agent
    print("🧠 Training Q-learning agent...")
    ai = TicTacToeAI(Strategy.Q_LEARNING, Strategy.RANDOM)
    ai.train_q_learning_agent(episodes=1000, opponent_strategy=Strategy.RANDOM)
    
    print("\n✅ Training complete! Agent learned from 1000 games.")
    print("📊 Q-table contains", len(ai.q_agent_x.q_table), "different game states")
    
    while True:
        print("\n" + "="*50)
        print("🎯 CHOOSE YOUR OPPONENT FOR Q-LEARNING AGENT:")
        print("1. 🎲 Random Player (Easy)")
        print("2. ⚔️  Aggressive Player (Medium)")
        print("3. 🛡️  Defensive Player (Hard)")
        print("4. 🧮 Minimax Expert (Impossible)")
        print("5. 🔄 Train more episodes")
        print("6. 📊 Show Q-values for current position")
        print("0. ❌ Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            print("👋 Thanks for testing the Q-learning agent!")
            break
        elif choice == "1":
            play_interactive_game(ai, Strategy.RANDOM, "Random Player")
        elif choice == "2":
            play_interactive_game(ai, Strategy.AGGRESSIVE, "Aggressive Player")
        elif choice == "3":
            play_interactive_game(ai, Strategy.DEFENSIVE, "Defensive Player")
        elif choice == "4":
            play_interactive_game(ai, Strategy.MINIMAX, "Minimax Expert")
        elif choice == "5":
            additional_training(ai)
        elif choice == "6":
            show_q_values_demo(ai)
        else:
            print("❌ Invalid choice. Please try again.")

def play_interactive_game(ai, opponent_strategy, opponent_name):
    print(f"\n🎮 Q-Learning Agent vs {opponent_name}")
    print("=" * 40)
    
    ai.strategy_x = Strategy.Q_LEARNING
    ai.strategy_o = opponent_strategy
    
    # Reset game
    ai.reset_board()
    move_count = 0
    
    print("🎯 Game starting... Q-Learning plays as X")
    
    while ai.gameState.status == 'playing':
        move_count += 1
        print(f"\n--- Move {move_count} ---")
        
        # Show current board
        ai.print_board()
        
        current_player = ai.gameState.currentPlayer
        if current_player == 'X':  # Q-Learning turn
            print("🧠 Q-Learning Agent thinking...")
            
            # Show Q-values for available moves
            state = ''.join(ai.gameState.board)
            available_moves = ai.get_available_moves()
            
            print("📊 Q-values for available moves:")
            q_values = []
            for move in available_moves:
                q_value = ai.q_agent_x.get_q_value(state, move)
                q_values.append((move, q_value))
                print(f"   Position {move}: {q_value:.3f}")
            
            # Find best move
            best_move = max(q_values, key=lambda x: x[1])
            print(f"🎯 Best move: Position {best_move[0]} (Q-value: {best_move[1]:.3f})")
            
            # Make the move
            time.sleep(1)  # Dramatic pause
            move = ai.get_move_by_strategy('X', Strategy.Q_LEARNING)
            ai.make_move(move, 'X')
            print(f"✅ Q-Learning plays position {move}")
            
        else:  # Opponent turn
            print(f"🎲 {opponent_name} thinking...")
            time.sleep(0.5)
            move = ai.get_move_by_strategy('O', opponent_strategy)
            ai.make_move(move, 'O')
            print(f"✅ {opponent_name} plays position {move}")
        
        # Check for game end
        winner = ai.check_winner()
        if winner:
            ai.gameState.status = 'won' if winner != 'Tie' else 'tie'
            ai.gameState.winner = winner
        elif ' ' not in ai.gameState.board:
            ai.gameState.status = 'tie'
            ai.gameState.winner = 'Tie'
        
        # Switch players
        ai.gameState.currentPlayer = 'O' if current_player == 'X' else 'X'
    
    # Show final result
    print("\n🏁 GAME OVER!")
    ai.print_board()
    
    if ai.gameState.winner == 'X':
        print("🎉 Q-Learning Agent WINS!")
    elif ai.gameState.winner == 'O':
        print(f"😔 {opponent_name} wins!")
    else:
        print("🤝 It's a TIE!")
    
    input("\nPress Enter to continue...")

def additional_training(ai):
    print("\n🎓 Additional Training Session")
    print("-" * 30)
    
    episodes = input("How many additional episodes? (default 500): ").strip()
    try:
        episodes = int(episodes) if episodes else 500
    except ValueError:
        episodes = 500
    
    opponent_choice = input("Train against (1=Random, 2=Aggressive, 3=Defensive): ").strip()
    opponent_map = {
        "1": Strategy.RANDOM,
        "2": Strategy.AGGRESSIVE, 
        "3": Strategy.DEFENSIVE
    }
    opponent = opponent_map.get(opponent_choice, Strategy.RANDOM)
    
    print(f"🧠 Training for {episodes} episodes...")
    ai.train_q_learning_agent(episodes=episodes, opponent_strategy=opponent)
    print(f"✅ Training complete! Q-table now has {len(ai.q_agent_x.q_table)} states")

def show_q_values_demo(ai):
    print("\n📊 Q-Values Demonstration")
    print("-" * 30)
    
    # Show Q-values for some interesting positions
    demo_positions = [
        ("         ", "Empty board"),
        ("X        ", "After opening move"),
        ("X   O    ", "Early game"),
        ("XX O     ", "Two in a row threat"),
        ("XOX      ", "Blocked line"),
        ("X O   O  ", "Multiple threats")
    ]
    
    for state, description in demo_positions:
        print(f"\n{description}: {state}")
        available_moves = [i for i in range(9) if state[i] == ' ']
        
        if available_moves:
            print("Q-values for available moves:")
            q_values = []
            for move in available_moves:
                q_value = ai.q_agent_x.get_q_value(state, move)
                q_values.append((move, q_value))
                print(f"  Position {move}: {q_value:7.3f}")
            
            if q_values:
                best_move = max(q_values, key=lambda x: x[1])
                print(f"🎯 Best choice: Position {best_move[0]} ({best_move[1]:.3f})")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        interactive_q_learning_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()