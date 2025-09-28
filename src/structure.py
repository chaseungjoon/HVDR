class HRMNode:
    """
    질의/문서 트리의 각 노드.
    - query: 이 노드에서 해결할 하위 질의
    - children: 하위 노드 리스트
    - evidence_docs: 이 노드에 관련된 문서 후보
    - score: 선택된 문서의 구조적 점수 p(d)
    """
    def __init__(self, query, children=None):
        self.query = query
        self.children = children if children else []
        self.evidence_docs = []
        self.score = 0.0

