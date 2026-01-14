#!/usr/bin/env python3
"""
View Statistics

Display matching statistics from the database.
"""

from app.services.matching_service import MatchingService


def main():
    """Display statistics."""
    print("📊 SalesAgent Statistics")
    print("=" * 60)
    
    service = MatchingService()
    
    try:
        stats = service.get_match_statistics()
        
        print(f"\n📈 Total Matches: {stats['total_matches']}")
        
        if stats['by_product']:
            print("\n🎯 Matches by Product:")
            for product, count in sorted(
                stats['by_product'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"  • {product}: {count}")
        
        print("\n📊 Score Distribution:")
        for range_name, count in stats['score_distribution'].items():
            bar = "█" * (count // 2) if count > 0 else ""
            print(f"  {range_name:8} | {bar} {count}")
        
        # Tender count
        tender_count = service.tender_repo.count()
        print(f"\n📋 Total Tenders in Database: {tender_count}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure MongoDB is running and accessible")


if __name__ == "__main__":
    main()
