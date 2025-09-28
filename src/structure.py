class HRMNode:
    """
    Hierarchical Reasoning Model (HRM)의 기본 노드 클래스

    속성:
        query (str): 이 노드에서 다루는 질의 또는 하위 질의
        children (list[HRMNode]): 하위 노드 리스트
        evidence_docs (dict): 문서 후보 {doc_id: score} 형태
        score (float): 이 노드에서 선택된 문서들의 구조적 점수 합
    """

    def __init__(self, query, children=None):
        """
        HRMNode 생성자

        Args:
            query (str): 이 노드에서 다룰 질의
            children (list[HRMNode], optional): 초기 children 노드
        """
        self.query = query
        self.children = children if children is not None else []
        self.evidence_docs = {}  # {문서ID: 점수}
        self.score = 0.0

    def add_child(self, child_node):
        """
        자식 노드 추가
        """
        if isinstance(child_node, HRMNode):
            self.children.append(child_node)
        else:
            raise TypeError("child_node must be an instance of HRMNode")

    def set_evidence_docs(self, evidence_docs):
        """
        문서 후보 저장
        Args:
            evidence_docs (dict): {doc_id: score}
        """
        if not isinstance(evidence_docs, dict):
            raise TypeError("evidence_docs must be a dict {doc_id: score}")
        self.evidence_docs = evidence_docs

    def select_top_k_docs(self, k=3):
        """
        점수가 높은 상위 k개의 문서를 선택하고 score 업데이트
        Returns:
            list: 선택된 문서 ID 리스트
        """
        if not self.evidence_docs:
            return []

        sorted_docs = sorted(
            self.evidence_docs.items(),
            key=lambda x: x[1],
            reverse=True
        )
        top_k = sorted_docs[:k]
        self.score = sum(score for _, score in top_k)
        return [doc_id for doc_id, _ in top_k]

    def traverse(self, depth=0):
        """
        트리 전체 구조를 보기 좋게 출력
        """
        indent = "  " * depth
        print(f"{indent}- Query: {self.query} | Score: {self.score:.4f}")
        if self.evidence_docs:
            top_docs = self.select_top_k_docs(k=3)
            print(f"{indent}  Evidence Docs (top 3): {top_docs}")
        for child in self.children:
            child.traverse(depth + 1)