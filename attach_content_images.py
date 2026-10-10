"""Attach approved illustrations to existing published content, preserving uploads."""
import io
import json
import subprocess
import sys
import time
from uuid import uuid4
from PIL import Image
from server import ROOT, DATA, db

TARGETS = [
    ('activities', 'activity-seminars', 'seminar'),
    ('activities', 'activity-competition-teams', 'team'),
    ('activities', 'activity-history-exploration', 'history'),
    ('projects', 'independence-network', 'history'),
    ('projects', 'andong-report', 'history'),
]


def attach():
    images = {}
    for _, _, asset in TARGETS:
        if asset not in images:
            with Image.open(ROOT / 'images' / 'activities' / (asset + '-ai.png')) as image:
                output = io.BytesIO()
                image.convert('RGB').save(output, format='WEBP', quality=88)
                images[asset] = output.getvalue()
    backup = DATA / ('before-illustration-attachments-' + uuid4().hex + '.sqlite3')
    subprocess.run([sys.executable, str(ROOT / 'manage.py'), 'backup', '--output', str(backup)], check=True)
    attached = skipped = missing = 0
    with db() as conn:
        conn.execute('BEGIN IMMEDIATE')
        for kind, key, asset in TARGETS:
            item_id = 'voda-20261010-' + key
            row = conn.execute('SELECT data FROM items WHERE id=? AND kind=?', (item_id, kind)).fetchone()
            if row is None:
                missing += 1
                continue
            item = json.loads(row['data'])
            if item.get('photos'):
                skipped += 1
                continue
            photo_id = str(uuid4())
            name = 'ai-generated-' + asset + '.webp'
            conn.execute('INSERT INTO photos VALUES(?,?,?,?)', (photo_id, name, images[asset], time.time()))
            item['photos'] = [{'id': photo_id, 'name': name, 'url': '/media/' + photo_id}]
            item['updatedAt'] = max(int(time.time() * 1000), item.get('updatedAt', 0) + 1)
            conn.execute('UPDATE items SET data=? WHERE id=?', (json.dumps(item, ensure_ascii=False), item_id))
            attached += 1
    print(f'Attached {attached}; preserved {skipped}; missing posts {missing}.')


if __name__ == '__main__':
    attach()
