"""Publish activity introductions; no invented event dates, photos or outcomes."""
from publish_content import publish

ACTIVITIES = [
    ('activities', 'activity-seminars', {
        'title': '함께 배우는 AI·데이터 분석 — 지부별 세미나',
        'description': 'VODA의 지부별 세미나는 AI와 데이터 분석을 함께 배우는 활동입니다. 다양한 전공의 관점으로 기술을 살펴보고, 데이터가 사회 문제를 이해하는 데 어떻게 쓰일 수 있는지 생각합니다.\n\n공개된 1.5기 활동 안내에서는 총 6회차의 지부 세미나 커리큘럼을 소개했습니다. 혼자 공부하며 생긴 질문을 함께 나누고, 배운 내용을 프로젝트로 연결하는 것이 활동의 방향입니다.\n\n이 글은 활동 소개이며 개별 회차의 진행 후기나 현재 일정 안내는 아닙니다.',
    }),
    ('activities', 'activity-competition-teams', {
        'title': '관심 있는 문제를 프로젝트로 — 공모전 TF',
        'description': '공모전 TF는 관심 있는 주제를 중심으로 팀을 구성해 공모전을 준비하는 VODA의 활동입니다. 서로 다른 전공과 경험을 가진 구성원이 함께 문제를 살펴보고, AI·데이터 분석을 활용할 방법을 탐색합니다.\n\n기술을 배우는 데서 한 걸음 더 나아가 누구에게 도움이 되는 프로젝트인지 고민하는 과정에 의미를 둡니다.\n\n이 글은 공모전 TF의 활동 방향을 소개합니다. 특정 대회 출전이나 수상 실적을 알리는 글은 아닙니다.',
    }),
    ('activities', 'activity-history-exploration', {
        'title': '데이터로 역사를 살펴보기 — 독립운동 자료 탐구',
        'description': 'VODA 홈페이지에 공개된 독립운동가 관계망과 안동 지역 독립운동 연구 보고서를 소개합니다. 인물·단체·사건 사이의 연결과 지역의 역사 기록을 함께 살펴볼 수 있는 자료입니다.\n\n관계망에서는 인물 검색과 연도 필터를 이용해 연결을 탐색할 수 있습니다. 연구 보고서에서는 안동 내앞마을과 풍산 일대의 독립운동, 신간회 안동지회, 역사적 평가와 서훈 과제를 다룹니다.\n\nProjects에서 관계망을 직접 조작하거나 보고서 본문을 읽어보세요. 이 글은 공개 자료 활용 안내이며 별도 오프라인 행사의 후기는 아닙니다.',
    }),
]

if __name__ == '__main__':
    publish(ACTIVITIES)
