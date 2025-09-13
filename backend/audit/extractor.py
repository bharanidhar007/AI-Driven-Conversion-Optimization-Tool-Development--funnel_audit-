from bs4 import BeautifulSoup
import re
CTA_PATTERNS = [r'get started', r'buy now', r'start free', r'book a demo', r'try free', r'sign up', r'get access']
def extract_headline(soup):
    h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True): return h1.get_text(strip=True)
    for sel in ['.hero h1', '.headline', 'header h1']:
        el = soup.select_one(sel)
        if el: return el.get_text(strip=True)
    texts = sorted([(len(t.get_text(strip=True)), t) for t in soup.find_all(['h1','h2','h3','p'])], reverse=True)
    return texts[0][1].get_text(strip=True) if texts else ''
def extract_ctas(soup):
    results=[]
    for tag in soup.find_all(['a','button','input']):
        txt = tag.get_text(strip=True) if tag.name!='input' else tag.get('value','')
        if not txt: continue
        for p in CTA_PATTERNS:
            if re.search(p, txt, re.I):
                results.append({'text':txt, 'html': str(tag)[:300]})
                break
    return results
def extract_testimonials(soup):
    sel = soup.find_all(string=re.compile(r'(testimonial|review|what our|customer story|case study|kudos)', re.I))
    t=[]
    for s in sel:
        parent = s.find_parent()
        t.append({'text': parent.get_text(" ",strip=True)[:400]})
    return t
def extract_urgency(soup):
    urgent = re.compile(r'\b(limited time|only \d+ left|hurry|ends in|today only|sale ends|while stocks last)\b', re.I)
    return [m.strip() for m in soup.find_all(string=urgent)]
def extract_social_proof(soup):
    brands=[]
    for img in soup.find_all('img', alt=True):
        alt = img['alt']
        if 'logo' in alt.lower() or len(alt) < 25:
            brands.append({'alt': alt, 'src': img.get('src')})
    icons = len(soup.select('a[href*="facebook"], a[href*="twitter"], a[href*="linkedin"], a[href*="instagram"]'))
    return {'brands': brands, 'social_icon_count': icons}
def run_extraction(scraped):
    soup = BeautifulSoup(scraped['html'],'html.parser')
    return {
        'headline': extract_headline(soup),
        'ctas': extract_ctas(soup),
        'testimonials': extract_testimonials(soup),
        'urgency': extract_urgency(soup),
        'social_proof': extract_social_proof(soup),
        'title': scraped.get('title'),
        'meta': scraped.get('meta'),
        'visible_text_sample': scraped.get('visible_text')[:2000]
    }
