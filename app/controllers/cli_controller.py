"""
CLI Controller for command-line interface.

Handles user interaction through command-line.
"""

import sys
from typing import Optional
from app.services import MatchingService
from app.utils import get_logger
from app.config import get_settings

logger = get_logger(__name__)


class CLIController:
    """
    Controller for CLI operations.
    
    Provides command-line interface for the application.
    """
    
    def __init__(self):
        """Initialize CLI controller."""
        self.settings = get_settings()
        self.matching_service = MatchingService()
        logger.info("Initialized CLIController")
    
    def run_matching(
        self,
        use_ai: bool = False,
        min_score: Optional[float] = None
    ) -> int:
        """
        Run matching workflow from CLI.
        
        Args:
            use_ai: Use AI matching
            min_score: Minimum score threshold
        
        Returns:
            int: Exit code (0 = success)
        """
        print("🚀 Starting SalesAgent Matching System")
        print("=" * 60)
        
        # Determine matching mode
        mode = "AI-Powered (LLM)" if use_ai else "Rule-Based"
        print(f"📊 Mode: {mode}")
        
        # Set min score
        if min_score is None:
            min_score = self.settings.min_match_score
        print(f"🎯 Minimum Score: {min_score}")
        print("=" * 60)
        
        try:
            # Execute matching
            matches = self.matching_service.execute_matching(
                use_ai=use_ai,
                min_score=min_score,
                save_results=True,
                export_json=True
            )
            
            # Display results
            print(f"\n✅ Matching Complete!")
            print(f"📈 Found {len(matches)} matches\n")
            
            if matches:
                print("Top Matches:")
                print("-" * 60)
                for i, match in enumerate(matches[:5], 1):
                    print(f"{i}. {match.tender_name}")
                    print(f"   Product: {match.matched_product}")
                    print(f"   Score: {match.score:.2f}")
                    print(f"   URL: {match.market_url}")
                    print()
                
                if len(matches) > 5:
                    print(f"... and {len(matches) - 5} more matches")
            
            # Show statistics
            stats = self.matching_service.get_match_statistics()
            print("\n📊 Statistics:")
            print(f"   Total Matches: {stats['total_matches']}")
            print(f"   Products Matched: {len(stats['by_product'])}")
            
            print("\n💾 Results saved to database and exported to JSON")
            
            return 0
            
        except Exception as e:
            logger.error(f"Matching failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            return 1
    
    def show_statistics(self) -> int:
        """
        Show matching statistics.
        
        Returns:
            int: Exit code
        """
        print("📊 SalesAgent Statistics")
        print("=" * 60)
        
        try:
            stats = self.matching_service.get_match_statistics()
            
            print(f"\nTotal Matches: {stats['total_matches']}")
            
            if stats['by_product']:
                print("\nMatches by Product:")
                for product, count in sorted(
                    stats['by_product'].items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    print(f"  {product}: {count}")
            
            print("\nScore Distribution:")
            for range_name, count in stats['score_distribution'].items():
                print(f"  {range_name}: {count}")
            
            return 0
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            print(f"\n❌ Error: {e}")
            return 1


def main():
    """Main CLI entry point."""
    controller = CLIController()
    
    # Parse simple command line arguments
    use_ai = "--ai" in sys.argv or "-a" in sys.argv
    show_stats = "--stats" in sys.argv or "-s" in sys.argv
    
    if show_stats:
        return controller.show_statistics()
    else:
        return controller.run_matching(use_ai=use_ai)


if __name__ == "__main__":
    sys.exit(main())
