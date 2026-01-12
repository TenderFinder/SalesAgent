"""
SalesAgent - Main Application Entry Point

Professional Agentic AI system for government tender matching.
"""

import sys
import argparse
from app.controllers import CLIController
from app.utils import get_logger
from app import __version__

logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser.
    
    Returns:
        ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description="SalesAgent - Intelligent Government Tender Matching System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run rule-based matching
  python main.py match

  # Run AI-powered matching
  python main.py match --ai

  # Run with custom minimum score
  python main.py match --min-score 2.0

  # Show statistics
  python main.py stats

  # Show version
  python main.py --version
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'SalesAgent {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Match command
    match_parser = subparsers.add_parser(
        'match',
        help='Run tender-product matching'
    )
    match_parser.add_argument(
        '--ai',
        '-a',
        action='store_true',
        help='Use AI-powered matching (requires Ollama)'
    )
    match_parser.add_argument(
        '--min-score',
        '-m',
        type=float,
        help='Minimum match score threshold'
    )
    
    # Stats command
    subparsers.add_parser(
        'stats',
        help='Show matching statistics'
    )
    
    return parser


def main():
    """Main application entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize controller
    controller = CLIController()
    
    # Route to appropriate command
    if args.command == 'match':
        logger.info(f"Running match command (ai={args.ai})")
        return controller.run_matching(
            use_ai=args.ai,
            min_score=args.min_score
        )
    
    elif args.command == 'stats':
        logger.info("Running stats command")
        return controller.show_statistics()
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
