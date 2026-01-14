"""
LLM-powered matching agent using Ollama.

Implements AI-powered matching with contextual understanding.
"""

import json
from typing import List, Dict, Any, Optional
import ollama

from app.models import Tender, Product, Match, LLMMatchResult
from app.agents.base_agent import BaseAgent
from app.config import get_llm_config
from app.utils import get_logger

logger = get_logger(__name__)


class LLMMatchingAgent(BaseAgent):
    """
    LLM-powered agent for intelligent tender-product matching.
    
    Uses Ollama to perform contextual analysis and matching with
    deeper understanding of tender requirements and product capabilities.
    
    Configuration:
        model: Ollama model name (default: llama3.2)
        min_score: Minimum score threshold (default: 50)
        timeout: Request timeout in seconds (default: 120)
        batch_size: Number of tenders to process at once
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize LLM matching agent.
        
        Args:
            config: Agent configuration
        """
        super().__init__(config)
        
        llm_config = get_llm_config()
        self.model = self.config.get('model', llm_config['model'])
        self.min_score = self.config.get('min_score', 50)
        self.timeout = self.config.get('timeout', llm_config['timeout'])
        self.batch_size = self.config.get('batch_size', 10)
        
        logger.info(f"Initialized {self.name} with model={self.model}, "
                   f"min_score={self.min_score}")
    
    def analyze(
        self,
        tenders: List[Tender],
        products: List[Product],
        **kwargs
    ) -> List[Match]:
        """
        Analyze tenders against products using LLM.
        
        Args:
            tenders: List of tenders to analyze
            products: List of products to match against
            **kwargs: Additional parameters
        
        Returns:
            List[Match]: List of matches found
        """
        logger.info(f"Starting LLM analysis: {len(tenders)} tenders, "
                   f"{len(products)} products")
        
        all_matches = []
        
        # Process in batches to avoid overwhelming the LLM
        for i in range(0, len(tenders), self.batch_size):
            batch_tenders = tenders[i:i + self.batch_size]
            logger.debug(f"Processing batch {i // self.batch_size + 1}: "
                        f"{len(batch_tenders)} tenders")
            
            batch_matches = self._analyze_batch(batch_tenders, products)
            all_matches.extend(batch_matches)
        
        logger.info(f"LLM analysis complete: found {len(all_matches)} matches")
        
        return self.postprocess_matches(all_matches)
    
    def _analyze_batch(
        self,
        tenders: List[Tender],
        products: List[Product]
    ) -> List[Match]:
        """
        Analyze a batch of tenders using LLM.
        
        Args:
            tenders: Batch of tenders
            products: Products to match against
        
        Returns:
            List[Match]: Matches found in batch
        """
        # Prepare data for LLM
        tenders_data = [
            {
                "id": t.id,
                "title": t.display_name,
                "description": t.description,
                "sla": t.sla,
                "tags": t.search_tags
            }
            for t in tenders
        ]
        
        products_data = [
            {
                "name": p.name,
                "keywords": p.keywords,
                "category": p.category,
                "description": p.description
            }
            for p in products
        ]
        
        # Build prompt
        prompt = self._build_prompt(tenders_data, products_data)
        
        # Call LLM
        try:
            llm_results = self._call_llm(prompt)
            
            # Convert LLM results to Match objects
            matches = self._convert_llm_results(llm_results, tenders)
            
            return matches
            
        except Exception as e:
            logger.error(f"Error in LLM analysis: {e}")
            return []
    
    def _build_prompt(
        self,
        tenders_data: List[Dict],
        products_data: List[Dict]
    ) -> str:
        """
        Build prompt for LLM.
        
        Args:
            tenders_data: Tender data for prompt
            products_data: Product data for prompt
        
        Returns:
            str: Formatted prompt
        """
        tenders_json = json.dumps(tenders_data, indent=2)
        products_json = json.dumps(products_data, indent=2)
        
        prompt = f"""You are a Sales Engineer analyzing government tenders to find viable sales opportunities.

AVAILABLE TENDERS:
{tenders_json}

COMPANY PRODUCTS:
{products_json}

Task:
1. For each tender, identify if any of our products can fulfill the requirement
2. Only return substantial matches (Matching Score > {self.min_score})
3. Analyze if the product needs customization
4. Provide clear reasoning for each match

Return ONLY a JSON list of objects in this exact format:
[
    {{
        "tender_id": "<id from tender list>",
        "tender_title": "<title from tender list>",
        "matched_product": "<product name>",
        "matching_score": <int 0-100>,
        "customization_possibility": "<string explanation>",
        "reasoning": "<short reasoning>"
    }}
]

If no matches are found, return an empty list [].
Do not include any other text, only the JSON array.
"""
        return prompt
    
    def _call_llm(self, prompt: str) -> List[LLMMatchResult]:
        """
        Call Ollama LLM with prompt.
        
        Args:
            prompt: Formatted prompt
        
        Returns:
            List[LLMMatchResult]: Parsed LLM results
        
        Raises:
            Exception: If LLM call fails
        """
        logger.debug(f"Calling Ollama model: {self.model}")
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            content = response['message']['content']
            logger.debug(f"LLM response received: {len(content)} characters")
            
            # Parse JSON from response
            results = self._parse_llm_response(content)
            
            return results
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _parse_llm_response(self, content: str) -> List[LLMMatchResult]:
        """
        Parse LLM response to extract match results.
        
        Args:
            content: Raw LLM response
        
        Returns:
            List[LLMMatchResult]: Parsed results
        """
        # Clean up markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        content = content.strip()
        
        try:
            data = json.loads(content)
            
            if not isinstance(data, list):
                logger.warning("LLM response is not a list, wrapping in list")
                data = [data] if data else []
            
            # Convert to LLMMatchResult objects
            results = [LLMMatchResult(**item) for item in data]
            
            logger.debug(f"Parsed {len(results)} match results from LLM")
            return results
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.debug(f"Response content: {content[:500]}")
            return []
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return []
    
    def _convert_llm_results(
        self,
        llm_results: List[LLMMatchResult],
        tenders: List[Tender]
    ) -> List[Match]:
        """
        Convert LLM results to Match objects.
        
        Args:
            llm_results: LLM match results
            tenders: Original tender objects (for URLs)
        
        Returns:
            List[Match]: Match objects
        """
        # Create tender ID to URL mapping
        tender_urls = {t.id: t.market_url for t in tenders}
        
        matches = []
        for llm_result in llm_results:
            market_url = tender_urls.get(llm_result.tender_id, "")
            match = llm_result.to_match(market_url=market_url)
            matches.append(match)
        
        return matches
    
    def postprocess_matches(self, matches: List[Match]) -> List[Match]:
        """
        Postprocess LLM matches.
        
        Args:
            matches: Raw matches
        
        Returns:
            List[Match]: Processed matches
        """
        # Filter by minimum score
        filtered = [m for m in matches if m.score >= self.min_score]
        
        # Sort by score
        filtered.sort(key=lambda m: m.score, reverse=True)
        
        logger.debug(f"Postprocessing: {len(matches)} -> {len(filtered)} matches "
                    f"(min_score={self.min_score})")
        
        return filtered
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get agent capabilities.
        
        Returns:
            Dict: Agent capabilities
        """
        capabilities = super().get_capabilities()
        capabilities.update({
            "matching_type": "ai-powered",
            "model": self.model,
            "min_score": self.min_score,
            "supports_batch": True,
            "supports_streaming": False,
            "contextual_understanding": True
        })
        return capabilities
