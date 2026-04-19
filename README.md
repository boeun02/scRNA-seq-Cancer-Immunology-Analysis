# 🧬 Multimodal Tumor Microenvironment Modeling

암 조직 내 세포 간 상호작용을  
Spatial Transcriptomics와 Single-cell 데이터를 기반으로 모델링하는 프로젝트입니다.

---

## 1. 🎯 Research Goal

- Spatial proximity와 gene expression similarity 간 관계 분석
- 세포 간 interaction graph 모델링
- Tumor Microenvironment(TME) 구조 이해

---

## 2. ❓ Research Question

> 공간적으로 가까운 세포들은 실제로 유전자적으로도 유사한가?

---

## 3. 📂 Project Structure


bio-cell-interaction-project/

├── notebooks/ # 분석 및 실험
│ ├── 01_exploration.ipynb
│ ├── 02_similarity.ipynb
│ └── 03_graph.ipynb
│
├── src/ # 핵심 로직
│ ├── preprocessing.py
│ ├── similarity.py
│ ├── graph_builder.py
│ └── gnn_model.py
│
├── app/ # (추후) 서비스 레이어
│ ├── backend/
│ └── frontend/
│
├── results/ # 결과 저장
│
├── README.md
└── requirements.txt


---

## 4. 🌿 Branch Strategy

| 브랜치 | 역할 |
|--------|------|
| main   | 최종 결과 (포트폴리오) |
| dev    | 개발 브랜치 |
| feature/* | 기능/실험 단위 |

---

## 5. 📝 Commit Convention

| 타입 | 설명 |
|------|------|
| feat | 기능 추가 |
| analysis | 데이터 분석 |
| fix | 버그 수정 |
| refactor | 코드 개선 |
| wip | 실험 중 |

---

## 6. 🛠 Tech Stack

- Python (Scanpy, PyTorch)
- Graph Neural Network
- FastAPI (예정)
- React (예정)

---

## 7. 📈 Project Roadmap

- [x] Data exploration
- [ ] Similarity analysis
- [ ] Graph modeling
- [ ] Multimodal integration
- [ ] Web visualization

---

## 8. 📊 Expected Outcome

- 세포 간 상호작용 구조를 반영한 그래프 모델
- TME 구조 시각화
- 연구 기반 분석 파이프라인 구축
