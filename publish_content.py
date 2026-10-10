"""Publish the five approved October 2026 posts on the selected VODA DB."""
import json
import subprocess
import sys
import time
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo
from server import ROOT, DATA, Content, db

POSTS = [
    ('projects', 'independence-network', {
        'title': '독립운동의 연결을 읽다 — 독립운동가 관계망',
        'description': '독립운동의 역사를 인물과 단체, 사건 사이의 연결로 살펴보는 데이터 시각화 프로젝트입니다.\n\n인물 208명, 단체 55개, 사건 50개와 관계 492개를 하나의 관계망에 담았습니다. 인물 검색과 연도 필터를 활용해 관심 있는 인물의 활동과 시대별 연결을 탐색할 수 있습니다.\n\nProjects의 독립운동가 관계망 탭에서 직접 확인해보세요.',
        'projectCategory': '역사 · 데이터 시각화',
        'link': 'https://voda-run.duckdns.org/analysis/',
    }),
    ('projects', 'andong-report', {
        'title': '안동 독립운동의 역사를 다시 읽다',
        'description': '안동 내앞마을과 풍산 일대의 독립운동을 살펴보고, 사회주의 계열 독립운동가의 역사적 평가와 서훈 과제를 검토한 연구 보고서입니다.\n\n혁신 유림의 변화부터 신간회 안동지회의 활동까지 관련 기록을 살펴보며, 독립운동의 다양한 흐름을 어떻게 기억할 것인지 질문합니다.\n\n보고서 본문은 웹에서 읽을 수 있으며, Word 파일로도 내려받을 수 있습니다.',
        'projectCategory': '역사 · 연구 보고서',
        'link': 'https://voda-run.duckdns.org/analysis/reports/andong/',
    }),
    ('board', 'website-guide', {
        'title': 'VODA 홈페이지 이용 안내',
        'content': 'VODA의 소식과 프로젝트를 한곳에서 만나보세요.\n\nAbout에서는 동아리의 방향과 주요 활동을, Activities에서는 등록된 활동 기록을 확인할 수 있습니다. Projects에서는 독립운동가 관계망과 연구 보고서를 살펴볼 수 있으며, 공지사항은 Board에서 안내합니다.\n\n데이터로 사회를 바라보는 VODA의 활동에 관심 부탁드립니다.',
        'category': 'notice',
    }),
    ('board', 'research-release', {
        'title': '독립운동가 관계망과 연구 보고서 공개 안내',
        'content': 'Projects에 독립운동가 관계망과 안동 지역 독립운동 연구 보고서를 공개했습니다.\n\n관계망에서는 인물을 검색하거나 연도를 조절하며 인물·단체·사건의 연결을 살펴볼 수 있습니다. 넓은 화면에서 탐색하려면 새 탭에서 크게 보기를 이용해주세요.\n\n함께 공개한 연구 보고서는 보고서 읽기와 Word 다운로드로 확인할 수 있습니다.',
        'category': 'notice',
    }),
    ('board', 'recruitment-channels', {
        'title': 'VODA 활동 및 모집 소식 확인 안내',
        'content': 'VODA는 다양한 전공의 대학생이 함께 AI와 데이터 분석을 배우고, 사회 문제를 탐구하는 연합 동아리입니다. 공개된 활동 안내에는 지부별 세미나와 공모전 TF 등이 소개되어 있습니다.\n\n현재 홈페이지에서는 모집 종료 상태를 안내하고 있습니다. 참여를 희망하는 분들은 Board와 인스타그램 @voda_data_ai에서 새로운 모집 공지를 확인해주세요.\n\n활동 안내: https://linkareer.com/activity/347618\n인스타그램: https://www.instagram.com/voda_data_ai/',
        'category': 'notice',
    }),
]


def publish(posts=None):
    posts = POSTS if posts is None else posts
    # Validate before taking a backup or writing any records.
    validated = [(kind, 'voda-20261010-' + key, Content(**value)) for kind, key, value in posts]
    backup = DATA / ('before-approved-posts-' + uuid4().hex + '.sqlite3')
    subprocess.run([sys.executable, str(ROOT / 'manage.py'), 'backup', '--output', str(backup)], check=True)
    inserted = 0
    now = int(time.time() * 1000)
    with db() as conn:
        conn.execute('BEGIN IMMEDIATE')
        for kind, item_id, body in validated:
            if conn.execute('SELECT 1 FROM items WHERE id=?', (item_id,)).fetchone():
                continue
            # Also skip a draft already entered by hand under a different ID.
            existing = conn.execute('SELECT data FROM items WHERE kind=?', (kind,)).fetchall()
            if any(json.loads(row['data']).get('title') == body.title for row in existing):
                continue
            item = {'id': item_id, 'title': body.title, 'createdAt': now, 'updatedAt': now}
            if kind == 'board':
                item.update(content=body.content, category=body.category, pinned=False,
                            date=datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y.%m.%d'))
            elif kind == 'projects':
                item.update(description=body.description, projectCategory=body.projectCategory, link=body.link, photos=[])
            else:
                item.update(description=body.description, photos=[])
            conn.execute('INSERT INTO items VALUES(?,?,?,?)', (item_id, kind, json.dumps(item, ensure_ascii=False), now))
            inserted += 1
    print(f'Published {inserted}; skipped {len(posts) - inserted}. Existing content preserved.')


if __name__ == '__main__':
    publish()
