"""
Concurrent Load Test - Simulate Multiple Interviews
Tests system performance with concurrent interviews
"""

import sys
import os
import asyncio
import time
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.src.init_free_ai import initialize_free_ai_system, get_ai_response_async, print_system_status


async def simulate_interview(interview_id, questions_per_interview=3):
    """Simulate one interview with multiple questions"""
    
    questions = [
        "Tell me about yourself and your background.",
        "What are your key strengths as a professional?",
        "Describe a challenging project you've worked on.",
        "Where do you see yourself in 5 years?",
        "Why should we hire you for this position?",
    ]
    
    responses = []
    start_time = time.time()
    
    try:
        # Ask random questions
        for i in range(questions_per_interview):
            question = questions[i % len(questions)]
            response = await get_ai_response_async(
                prompt=question,
                context="You are an AI interviewer conducting a professional interview."
            )
            responses.append(response)
        
        duration = time.time() - start_time
        return {
            'interview_id': interview_id,
            'success': True,
            'duration': duration,
            'questions': questions_per_interview
        }
        
    except Exception as e:
        duration = time.time() - start_time
        return {
            'interview_id': interview_id,
            'success': False,
            'duration': duration,
            'error': str(e)
        }


async def run_concurrent_test(num_concurrent=10, questions_per_interview=3):
    """Run concurrent interview simulation"""
    
    print("\n" + "="*70)
    print(f"CONCURRENT LOAD TEST - {num_concurrent} Interviews")
    print("="*70 + "\n")
    
    # Initialize system
    print("Initializing AI system...")
    ai_manager = initialize_free_ai_system()
    
    if not ai_manager or not ai_manager.providers:
        print("❌ No AI providers available. Please configure API keys.")
        return
    
    print(f"✓ System ready with {len(ai_manager.providers)} provider(s)\n")
    
    # Run concurrent interviews
    print(f"Starting {num_concurrent} concurrent interviews...")
    print(f"Each interview: {questions_per_interview} questions")
    print(f"Total requests: {num_concurrent * questions_per_interview}\n")
    
    start_time = time.time()
    
    # Execute all interviews concurrently
    results = await asyncio.gather(*[
        simulate_interview(i, questions_per_interview)
        for i in range(num_concurrent)
    ])
    
    total_duration = time.time() - start_time
    
    # Analyze results
    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])
    avg_duration = sum(r['duration'] for r in results) / len(results)
    
    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70 + "\n")
    
    print(f"📊 Performance Metrics:")
    print(f"  Total Interviews: {num_concurrent}")
    print(f"  Successful: {successful} ({successful/num_concurrent*100:.1f}%)")
    print(f"  Failed: {failed}")
    print(f"  Total Duration: {total_duration:.2f}s")
    print(f"  Avg Interview Duration: {avg_duration:.2f}s")
    print(f"  Throughput: {num_concurrent/total_duration:.1f} interviews/second")
    print()
    
    # Show system stats
    print("="*70)
    print("SYSTEM STATISTICS")
    print("="*70)
    print_system_status()
    
    # Capacity analysis
    print("\n" + "="*70)
    print("CAPACITY ANALYSIS")
    print("="*70 + "\n")
    
    stats = ai_manager.get_stats()
    total_requests = stats['total_requests']
    cache_hit_rate = stats.get('cache_hit_rate', 0)
    
    print(f"📈 Load Handling:")
    print(f"  Concurrent Interviews: {num_concurrent}")
    print(f"  Total API Requests: {total_requests}")
    print(f"  Cache Hit Rate: {cache_hit_rate:.1f}%")
    print(f"  Actual API Calls: {total_requests - stats['cache_hits']}")
    print()
    
    # Calculate capacity
    if 'huggingface' in ai_manager.providers:
        hf_accounts = len(ai_manager.providers['huggingface'].clients)
        hourly_capacity = hf_accounts * 1000  # ~1000 req/hour per account
        
        requests_per_hour = (total_requests / total_duration) * 3600
        utilization = (requests_per_hour / hourly_capacity) * 100
        
        print(f"💡 Capacity Insights:")
        print(f"  HF Accounts: {hf_accounts}")
        print(f"  Hourly Capacity: ~{hourly_capacity:,} requests/hour")
        print(f"  Current Load: ~{requests_per_hour:.0f} requests/hour")
        print(f"  Utilization: {utilization:.1f}%")
        print()
        
        # Recommendations
        if utilization > 80:
            print(f"⚠️  High utilization! Consider adding more accounts.")
        elif utilization > 50:
            print(f"✓ Good utilization. System has headroom.")
        else:
            print(f"✓ Low utilization. System can handle much more load!")
    
    print()
    
    # Show failures if any
    if failed > 0:
        print("\n❌ Failed Interviews:")
        for r in results:
            if not r['success']:
                print(f"  Interview {r['interview_id']}: {r['error']}")
    
    return successful == num_concurrent


def main():
    """Main test runner"""
    
    import argparse
    parser = argparse.ArgumentParser(description='Test concurrent interview load')
    parser.add_argument('--interviews', type=int, default=10, 
                       help='Number of concurrent interviews (default: 10)')
    parser.add_argument('--questions', type=int, default=3,
                       help='Questions per interview (default: 3)')
    
    args = parser.parse_args()
    
    print(f"\n🧪 Testing with {args.interviews} concurrent interviews...")
    print(f"   Each interview will ask {args.questions} questions")
    print(f"   Total API requests: {args.interviews * args.questions}")
    
    try:
        success = asyncio.run(run_concurrent_test(
            num_concurrent=args.interviews,
            questions_per_interview=args.questions
        ))
        
        if success:
            print("\n" + "="*70)
            print("✅ ALL INTERVIEWS COMPLETED SUCCESSFULLY!")
            print("="*70)
            print("\nYour system can handle this load! 🎉")
            sys.exit(0)
        else:
            print("\n⚠️  Some interviews failed. Check logs above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
