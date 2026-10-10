"""Remove the requested editorial sentences without replacing user content."""
PHRASES = (
    '이 글은 활동 소개이며 개별 회차의 진행 후기나 현재 일정 안내는 아닙니다.',
    '이 글은 공모전 TF의 활동 방향을 소개합니다. 특정 대회 출전이나 수상 실적을 알리는 글은 아닙니다.',
    'Projects에서 관계망을 직접 조작하거나 보고서 본문을 읽어보세요.',
    '이 글은 공개 자료 활용 안내이며 별도 오프라인 행사의 후기는 아닙니다.',
)


def clean_text(text):
    for phrase in PHRASES:
        text = text.replace(phrase, '')
    return text.rstrip()


def cleanup():
    import json
    import subprocess
    import sys
    import time
    from uuid import uuid4
    from server import ROOT, DATA, db
    backup = DATA / ('before-copy-cleanup-' + uuid4().hex + '.sqlite3')
    subprocess.run([sys.executable, str(ROOT / 'manage.py'), 'backup', '--output', str(backup)], check=True)
    updated = 0
    with db() as conn:
        conn.execute('BEGIN IMMEDIATE')
        for row in conn.execute("SELECT id,data FROM items WHERE kind='activities'").fetchall():
            item = json.loads(row['data'])
            old = item.get('description', '')
            if not any(phrase in old for phrase in PHRASES):
                continue
            item['description'] = clean_text(old)
            item['updatedAt'] = max(int(time.time()*1000), item.get('updatedAt',0)+1)
            conn.execute('UPDATE items SET data=? WHERE id=?', (json.dumps(item,ensure_ascii=False),row['id']))
            updated += 1
    print(f'Cleaned {updated} activity descriptions. Images and other content preserved.')


if __name__ == '__main__':
    cleanup()
