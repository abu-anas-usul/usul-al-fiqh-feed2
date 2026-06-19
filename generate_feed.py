import json
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
import html

def generate_rss():
    with open('research.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'خلاصات أبحاث أصول الفقه - أبو أنس'
    ET.SubElement(channel, 'link').text = 'https://abu-anas-usul.github.io/usul-al-fiqh-feed/'
    ET.SubElement(channel, 'description').text = 'ثلاثة أبحاث جديدة يومياً في أصول الفقه'
    ET.SubElement(channel, 'language').text = 'ar'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
    atom_link.set('href', 'https://abu-anas-usul.github.io/usul-al-fiqh-feed/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    for research in data['researches']:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = research['title']
        ET.SubElement(item, 'link').text = 'https://abu-anas-usul.github.io/usul-al-fiqh-feed/'
        ET.SubElement(item, 'guid').text = f"research-{hash(research['title'])}"
        ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        description = f"""
        <h2 style="color:#1e5128;">المشكلة البحثية</h2>
        <p>{research['problem']}</p>
        
        <h2 style="color:#1e5128;">الملخص</h2>
        <p>{research['summary']}</p>
        
        <h2 style="color:#1e5128;">المنهجية</h2>
        <p>{research['methodology']}</p>
        
        <h2 style="color:#1e5128;">النتائج</h2>
        <p>{research['results']}</p>
        
        <h2 style="color:#1e5128;">التوصيات</h2>
        <p>{research['recommendations']}</p>
        
        <h2 style="color:#1e5128;">التقييم النقدي</h2>
        <p><strong style="color:#2e7d32;">✅ نقاط القوة:</strong> {research['strengths']}</p>
        <p><strong style="color:#c62828;">⚠️ نقاط الضعف:</strong> {research['weaknesses']}</p>
        
        <h2 style="color:#1e5128;">💡 أفكار مستوحاة لأبحاث الترقية</h2>
        <p>{research['suggestions']}</p>
        """
        
        desc_elem = ET.SubElement(item, 'description')
        desc_elem.text = description
    
    xml_str = minidom.parseString(ET.tostring(rss, encoding='unicode')).toprettyxml(indent='  ')
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print("✅ تم إنشاء feed.xml بنجاح")

if __name__ == '__main__':
    generate_rss()
