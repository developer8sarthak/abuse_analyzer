import json
from app.scraper import ContentScraper
from app.analyzer import AbuseAnalyzer

def main():
    try:
        with open('data/ruleset.json', 'r') as f:
            ruleset_data = json.load(f)
    except FileNotFoundError:
        print("Error: data/ruleset.json not found!")
        return

    scraper = ContentScraper()
    analyzer = AbuseAnalyzer(ruleset_data)

    url = input("Enter the URL to scan (include http/https): ").strip()
    
    print(f"\n--- Scanning: {url} ---")
    
    try:
        raw_text = scraper.get_text_from_url(url)
        
        results = analyzer.analyze(raw_text)

        print(f"\n[FINAL ABUSE SCORE: {results['overall_abuse_score']}/100]")
        print(f"AI Confidence: {results['ai_confidence']}%")
        print("\nBreakdown by Category:")
        for cat, data in results['breakdown'].items():
            print(f" - {cat.replace('_', ' ').title()}: {data['intensity_score']}% ({data['matches_found']} matches)")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()