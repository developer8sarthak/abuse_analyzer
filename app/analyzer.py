import re
from profanity_check import predict_prob

class AbuseAnalyzer:
    def __init__(self, ruleset_data):
        # Look for the 'rules' key in your JSON
        # If it doesn't exist, use an empty dictionary to avoid crashing
        self.rules = ruleset_data.get('rules', {})

    def analyze(self, text):
        results = {}
        total_violation_score = 0
        
        # 1. AI Layer: General Toxicity Check
        # Returns a probability from 0.0 to 1.0
        ai_score = predict_prob([text])[0] * 100

        # 2. Ruleset Layer: Categorized Regex Matching
        # We divide by word count to get a percentage
        word_list = text.split()
        total_words = len(word_list) if len(word_list) > 0 else 1

        for category, config in self.rules.items():
            # Combine all patterns into one search string
            all_patterns = config.get('patterns', []) + config.get('leet_speak', [])
            if not all_patterns:
                continue
                
            regex = re.compile(r'|'.join(all_patterns), re.IGNORECASE)
            matches = regex.findall(text)
            
            # Calculate score based on frequency and weight
            intensity = (len(matches) / total_words) * 100 * config.get('weight', 1.0)
            
            results[category] = {
                "matches_found": len(matches),
                "intensity_score": round(min(intensity, 100), 2)
            }
            total_violation_score += intensity

        # 3. Final Composite Score
        final_score = (ai_score * 0.5) + (total_violation_score * 0.5)
        
        return {
            "overall_abuse_score": round(min(final_score, 100), 2),
            "ai_confidence": round(ai_score, 2),
            "breakdown": results
        }