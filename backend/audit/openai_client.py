import os, json
import openai
openai.api_key = os.getenv('OPENAI_API_KEY','')
PROMPT_INSTRUCTIONS = """You are an expert Conversion Rate Optimization consultant.
Input: JSON object with extracted elements and signals.
Tasks:
1) Score the page 0-100.
2) For elements (headline, primary_cta, social_proof, testimonials, urgency, pricing, forms), classify PRESENT/MISSING/WEAK and severity 1-5.
3) Provide top 3 urgent fixes with copy/HTML snippets.
4) Provide 5 A/B test ideas, each with expected impact (low/med/high).
5) Provide 3 headline rewrites and 3 CTA rewrites.
Output: JSON with keys: score, elements, urgent_fixes, tests, rewrites, notes.
"""
def evaluate_with_openai(features_json):
    prompt = PROMPT_INSTRUCTIONS + "\nINPUT_JSON:\n" + json.dumps(features_json)
    try:
        resp = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL','gpt-4o'),
            messages=[{'role':'system','content':'You are a CRO consultant.'},
                      {'role':'user','content':prompt}],
            temperature=0.0,
            max_tokens=1200
        )
        text = resp['choices'][0]['message']['content']
        try:
            return json.loads(text)
        except Exception:
            return {'raw': text}
    except Exception as e:
        return {'error': str(e)}
