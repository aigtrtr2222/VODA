"""Run publication in a separate process and temporary DB, never operator data."""
import os
from pathlib import Path
import subprocess
import sys


def test_approved_image_attachments(tmp_path):
    root = Path(__file__).resolve().parents[1]
    script = '''
import json
from pathlib import Path
from server import db, DATA, app, Content, save
from fastapi.testclient import TestClient
from publish_content import publish
from publish_activities import ACTIVITIES
from attach_content_images import attach
publish()
publish(ACTIVITIES)
attach()
client = TestClient(app)
for kind, count in [('activities',3),('projects',2)]:
    items = client.get('/api/content/'+kind).json()
    assert len(items)==count
    for item in items:
        assert len(item['photos'])==1
        response=client.get(item['photos'][0]['url'])
        assert response.status_code==200 and response.headers['content-type']=='image/webp'
        assert response.content[:4]==b'RIFF'
        # Normal admin save must retain the attachment and attribution name.
        data={k:v for k,v in item.items() if k in Content.model_fields}
        data['photos']=[{'id':item['photos'][0]['id']}]
        saved=save(kind,Content(**data),item['id'])
        assert saved['photos']==item['photos']
with db() as c:
    before=[tuple(r) for r in c.execute('SELECT * FROM items ORDER BY id')]
attach()
with db() as c:
    assert c.execute('SELECT count(*) FROM photos').fetchone()[0]==5
    assert before==[tuple(r) for r in c.execute('SELECT * FROM items ORDER BY id')]
assert len(list(DATA.glob('before-illustration-attachments-*.sqlite3')))==2
'''
    subprocess.run([sys.executable, '-c', script], cwd=root,
                   env={**os.environ, 'VODA_DATA_DIR':str(tmp_path), 'PYTHONIOENCODING':'utf-8'}, check=True)
