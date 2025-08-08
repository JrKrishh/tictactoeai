#!/usr/bin/env python3
"""
Large-Scale AI vs AI Tic-Tac-Toe Training Data Generator
========================================================
Generates massive datasets for machine learning and AI research
"""

import multiprocessing as mp
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import threading
from queue import Queue
import gc
from collections import defaultdict
from tictactoe_ai import TicTacToeAI, Strategy, GameRecord, GameplayDataCollector
import time
from datetime import datetime
import json
import csv

class LargeScaleTrainingGenerator:
    """Large-scale training data generator with parallel processing"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or mp.cpu_count()
        self.data_collector = GameplayDataCollector()
        self.batch_size = 1000  # Games per batch
        self.total_games_generated = 0
        
    def generate_game_batch(self, strategy_pair: tuple, num_games: int, batch_id: int) -> list:
        """Generate a batch of games in a separate process"""
        ai = TicTacToeAI(strategy_pair[0], strategy_pair[1])
        batch_games = []
        
        for i in range(num_games):
            game_id = batch_id * self.batch_size + i
            ai.data_collector.current_game_id = game_id
            
            # Play game and collect data
            winner = ai.play_self_game(collect_data=True)
            
            # Get the recorded game
            if ai.data_collector.games_data:
                game_record = ai.data_collector.games_data[-1]
                batch_games.append(game_record)
        
        return batch_games
    
    def generate_massive_dataset(self, 
                               strategy_combinations: list,
                               games_per_combination: int = 5000,
                               output_prefix: str = "massive_training_data") -> dict:
        """Generate massive training dataset using parallel processing"""
        
        print("🚀 LARGE-SCALE AI vs AI TRAINING DATA GENERATION")
        print("=" * 70)
        
        total_combinations = len(strategy_combinations)
        total_games = total_combinations * games_per_combination
        
        print(f"📊 Generation Parameters:")
        print(f"  Strategy combinations: {total_combinations}")
        print(f"  Games per combination: {games_per_combination:,}")
        print(f"  Total games to generate: {total_games:,}")
        print(f"  Parallel workers: {self.max_workers}")
        print(f"  Batch size: {self.batch_size}")
        
        start_time = time.time()
        all_games = []
        
        # Process each strategy combination
        for combo_idx, (strat_x, strat_o) in enumerate(strategy_combinations):
            print(f"\n🎯 Processing combination {combo_idx + 1}/{total_combinations}")
            print(f"   {strat_x.value} vs {strat_o.value}")
            
            combo_start = time.time()
            combo_games = []
            
            # Calculate batches needed
            num_batches = (games_per_combination + self.batch_size - 1) // self.batch_size
            
            # Generate batches in parallel
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for batch_idx in range(num_batches):
                    games_in_batch = min(self.batch_size, 
                                       games_per_combination - batch_idx * self.batch_size)
                    
                    if games_in_batch > 0:
                        future = executor.submit(
                            self.generate_game_batch,
                            (strat_x, strat_o),
                            games_in_batch,
                            combo_idx * num_batches + batch_idx
                        )
                        futures.append(future)
                
                # Collect results
                completed_batches = 0
                for future in as_completed(futures):
                    batch_games = future.result()
                    combo_games.extend(batch_games)
                    completed_batches += 1
                    
                    if completed_batches % 5 == 0:
                        progress = completed_batches / len(futures) * 100
                        elapsed = time.time() - combo_start
                        print(f"     Batch progress: {completed_batches}/{len(futures)} ({progress:.1f}%) - {elapsed:.1f}s")
            
            all_games.extend(combo_games)
            combo_time = time.time() - combo_start
            games_per_sec = len(combo_games) / combo_time
            
            print(f"   ✅ Completed: {len(combo_games):,} games in {combo_time:.1f}s ({games_per_sec:.1f} games/sec)")
            
            # Periodic garbage collection for memory management
            gc.collect()
        
        # Store all games in data collector
        self.data_collector.games_data = all_games
        self.total_games_generated = len(all_games)
        
        total_time = time.time() - start_time
        overall_rate = self.total_games_generated / total_time
        
        print(f"\n🎉 GENERATION COMPLETED!")
        print(f"   Total games generated: {self.total_games_generated:,}")
        print(f"   Total time: {total_time:.1f} seconds")
        print(f"   Overall rate: {overall_rate:.1f} games/second")
        
        # Export data
        self.export_massive_dataset(output_prefix)
        
        # Generate comprehensive statistics
        stats = self.analyze_massive_dataset()
        
        return stats
    
    def export_massive_dataset(self, prefix: str):
        """Export massive dataset with optimized file handling"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n💾 Exporting massive dataset...")
        
        # Export to CSV with chunking for memory efficiency
        csv_filename = f"{prefix}_{timestamp}.csv"
        self.export_chunked_csv(csv_filename)
        
        # Export metadata and sample to JSON
        json_filename = f"{prefix}_metadata_{timestamp}.json"
        self.export_metadata_json(json_filename)
        
        # Export compressed summary
        summary_filename = f"{prefix}_summary_{timestamp}.json"
        self.export_summary(summary_filename)
        
        print(f"✅ Export completed:")
        print(f"   📄 Full dataset: {csv_filename}")
        print(f"   📋 Metadata: {json_filename}")
        print(f"   📊 Summary: {summary_filename}")
    
    def export_chunked_csv(self, filename: str, chunk_size: int = 10000):
        """Export CSV in chunks to handle large datasets efficiently"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['game_id', 'player_x_strategy', 'player_o_strategy', 
                         'winner', 'game_length', 'timestamp', 'moves_sequence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for i in range(0, len(self.data_collector.games_data), chunk_size):
                chunk = self.data_collector.games_data[i:i + chunk_size]
                
                for game in chunk:
                    moves_str = ';'.join([f"{state},{move},{player}" 
                                        for state, move, player in game.moves])
                    writer.writerow({
                        'game_id': game.game_id,
                        'player_x_strategy': game.player_x_strategy,
                        'player_o_strategy': game.player_o_strategy,
                        'winner': game.winner,
                        'game_length': game.game_length,
                        'timestamp': game.timestamp,
                        'moves_sequence': moves_str
                    })
                
                # Progress indicator
                progress = min(i + chunk_size, len(self.data_collector.games_data))
                print(f"   CSV export progress: {progress:,}/{len(self.data_collector.games_data):,}")
    
    def export_metadata_json(self, filename: str, sample_size: int = 100):
        """Export metadata and sample games to JSON"""
        strategies_used = list(set([g.player_x_strategy for g in self.data_collector.games_data] + 
                                 [g.player_o_strategy for g in self.data_collector.games_data]))
        
        # Sample games for JSON (to avoid huge files)
        sample_games = self.data_collector.games_data[:sample_size]
        
        metadata = {
            'generation_info': {
                'total_games': len(self.data_collector.games_data),
                'export_timestamp': datetime.now().isoformat(),
                'strategies_used': strategies_used,
                'sample_size': len(sample_games)
            },
            'sample_games': [
                {
                    'game_id': game.game_id,
                    'player_x_strategy': game.player_x_strategy,
                    'player_o_strategy': game.player_o_strategy,
                    'moves': [{'board_state': state, 'move': move, 'player': player} 
                             for state, move, player in game.moves],
                    'winner': game.winner,
                    'game_length': game.game_length,
                    'timestamp': game.timestamp
                } for game in sample_games
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def export_summary(self, filename: str):
        """Export comprehensive summary statistics"""
        stats = self.analyze_massive_dataset()
        
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def analyze_massive_dataset(self) -> dict:
        """Analyze the massive dataset for comprehensive statistics"""
        if not self.data_collector.games_data:
            return {"error": "No games in dataset"}
        
        print(f"\n🔍 Analyzing massive dataset ({len(self.data_collector.games_data):,} games)...")
        
        stats = {
            'dataset_info': {
                'total_games': len(self.data_collector.games_data),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'strategy_performance': defaultdict(lambda: {'games': 0, 'wins': 0, 'win_rate': 0.0}),
            'matchup_matrix': defaultdict(lambda: {'X_wins': 0, 'O_wins': 0, 'ties': 0, 'total': 0}),
            'game_characteristics': {
                'length_distribution': defaultdict(int),
                'average_length': 0.0,
                'opening_moves': defaultdict(int),
                'winning_patterns': defaultdict(int)
            }
        }
        
        total_length = 0
        
        for game in self.data_collector.games_data:
            # Strategy performance
            x_strat = game.player_x_strategy
            o_strat = game.player_o_strategy
            
            stats['strategy_performance'][x_strat]['games'] += 1
            stats['strategy_performance'][o_strat]['games'] += 1
            
            if game.winner == 'X':
                stats['strategy_performance'][x_strat]['wins'] += 1
            elif game.winner == 'O':
                stats['strategy_performance'][o_strat]['wins'] += 1
            
            # Matchup matrix
            matchup = f"{x_strat}_vs_{o_strat}"
            stats['matchup_matrix'][matchup]['total'] += 1
            
            if game.winner == 'X':
                stats['matchup_matrix'][matchup]['X_wins'] += 1
            elif game.winner == 'O':
                stats['matchup_matrix'][matchup]['O_wins'] += 1
            else:
                stats['matchup_matrix'][matchup]['ties'] += 1
            
            # Game characteristics
            stats['game_characteristics']['length_distribution'][game.game_length] += 1
            total_length += game.game_length
            
            # Opening moves
            if game.moves:
                first_move = game.moves[0][1]
                stats['game_characteristics']['opening_moves'][first_move] += 1
            
            # Winning patterns (game length for wins)
            if game.winner != 'Tie':
                stats['game_characteristics']['winning_patterns'][game.game_length] += 1
        
        # Calculate win rates
        for strategy in stats['strategy_performance']:
            data = stats['strategy_performance'][strategy]
            if data['games'] > 0:
                data['win_rate'] = data['wins'] / data['games'] * 100
        
        # Calculate average game length
        stats['game_characteristics']['average_length'] = total_length / len(self.data_collector.games_data)
        
        # Convert defaultdicts to regular dicts for JSON serialization
        stats['strategy_performance'] = dict(stats['strategy_performance'])
        stats['matchup_matrix'] = dict(stats['matchup_matrix'])
        stats['game_characteristics']['length_distribution'] = dict(stats['game_characteristics']['length_distribution'])
        stats['game_characteristics']['opening_moves'] = dict(stats['game_characteristics']['opening_moves'])
        stats['game_characteristics']['winning_patterns'] = dict(stats['game_characteristics']['winning_patterns'])
        
        return stats

def create_comprehensive_strategy_combinations():
    """Create comprehensive list of strategy combinations for large-scale generation"""
    all_strategies = list(Strategy)
    combinations = []
    
    # All unique pairs (including self-play)
    for i, strat_x in enumerate(all_strategies):
        for j, strat_o in enumerate(all_strategies):
            combinations.append((strat_x, strat_o))
    
    return combinations

def run_massive_generation():
    """Run massive training data generation"""
    print("🎯 MASSIVE AI vs AI TRAINING DATA GENERATION")
    print("=" * 70)
    
    # Initialize generator
    generator = LargeScaleTrainingGenerator()
    
    # Create strategy combinations
    combinations = create_comprehensive_strategy_combinations()
    
    print(f"📋 Strategy combinations to process: {len(combinations)}")
    for i, (x, o) in enumerate(combinations[:10]):  # Show first 10
        print(f"   {i+1:2d}. {x.value} vs {o.value}")
    if len(combinations) > 10:
        print(f"   ... and {len(combinations) - 10} more combinations")
    
    # Configuration
    games_per_combination = 500  # Start with smaller number for demo
    
    print(f"\n⚙️  Configuration:")
    print(f"   Games per combination: {games_per_combination:,}")
    print(f"   Total games: {len(combinations) * games_per_combination:,}")
    print(f"   Estimated time: ~{(len(combinations) * games_per_combination) / 1000:.1f} minutes")
    
    # Generate massive dataset
    stats = generator.generate_massive_dataset(
        combinations, 
        games_per_combination,
        "massive_tictactoe_training"
    )
    
    # Print final statistics
    print(f"\n📊 FINAL STATISTICS:")
    print(f"   Dataset size: {stats['dataset_info']['total_games']:,} games")
    print(f"   Average game length: {stats['game_characteristics']['average_length']:.1f} moves")
    
    print(f"\n🏆 Top performing strategies:")
    sorted_strategies = sorted(stats['strategy_performance'].items(), 
                              key=lambda x: x[1]['win_rate'], reverse=True)
    for strategy, data in sorted_strategies[:5]:
        print(f"   {strategy:12}: {data['win_rate']:5.1f}% win rate ({data['wins']:,}/{data['games']:,})")
    
    return stats

if __name__ == "__main__":
    # Run massive generation
    stats = run_massive_generation()