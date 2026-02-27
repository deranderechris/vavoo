#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
ADDONS_XML = os.path.join(REPO_PATH, 'addons.xml')

# Mapping: Addon-ID -> (ZIP-Ordner, ZIP-Dateiname)
ZIP_MAP = {
    'plugin.video.vavooto': ('plugin.video.vavooto', 'plugin.video.vavooto-2025.11.10-2.zip'),
}

def parse_addons(addons_xml):
    tree = ET.parse(addons_xml)
    root = tree.getroot()
    addons = []
    for addon in root.findall('addon'):
        addon_id = addon.get('id')
        name = addon.get('name')
        version = addon.get('version')
        summary = ''
        for ext in addon.findall('extension'):
            if ext.get('point') == 'xbmc.addon.metadata':
                summary_elem = ext.find('summary')
                if summary_elem is not None:
                    summary = summary_elem.text
        zip_folder, zip_file = ZIP_MAP.get(addon_id, (None, None))
        addons.append({
            'id': addon_id,
            'name': name,
            'version': version,
            'summary': summary,
            'zip_folder': zip_folder,
            'zip_file': zip_file
        })
    return addons

def generate_html(addons):
    rows = ''
    for addon in addons:
        zip_link = f"{addon['zip_folder']}/{addon['zip_file']}" if addon['zip_folder'] and addon['zip_file'] else '#'
        rows += f"<tr><td>{addon['name']}</td><td>{addon['version']}</td><td><a class='zip-link' href='{zip_link}' download>ZIP</a></td><td>{addon['summary']}</td></tr>\n"
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>VAVOO.TO Kodi Repository – Addon-Liste</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{ font-family: Arial, sans-serif; background: #181818; color: #eee; margin: 0; padding: 0; }}
    .container {{ max-width: 900px; margin: 40px auto; background: #232323; border-radius: 10px; box-shadow: 0 2px 8px #0008; padding: 32px; }}
    h1 {{ color: #ffb300; }}
    table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid #333; }}
    th {{ color: #ffb300; text-align: left; }}
    tr:last-child td {{ border-bottom: none; }}
    .info {{ margin-top: 32px; font-size: 0.95em; color: #aaa; }}
    .zip-link {{ color: #ffb300; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>VAVOO.TO Kodi Repository</h1>
    <table>
      <tr>
        <th>Addon</th>
        <th>Version</th>
        <th>Download</th>
        <th>Beschreibung</th>
      </tr>
      {rows}
    </table>
    <div class="info">
      <p>Füge folgende Repo-URL in Kodi hinzu (als Quelle):<br>
        <code>https://DEINE-URL-ODER-IP/repo/</code>
      </p>
      <p>© 2026 edit by der andere</p>
    </div>
  </div>
</body>
</html>'''
    return html

if __name__ == '__main__':
    addons = parse_addons(ADDONS_XML)
    html = generate_html(addons)
    with open(os.path.join(REPO_PATH, 'index.html'), 'w') as f:
        f.write(html)
    print('index.html wurde automatisch generiert.')
