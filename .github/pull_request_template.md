# 🧠 Summary

> 이번 PR에서 수행한 작업을 한 줄로 요약

---

# 🎯 Motivation (왜 했는가)

- 이 작업을 하게 된 배경
- 해결하고자 했던 문제
- 기존 한계점

예)
- Spatial 데이터에서 세포 간 관계를 정량적으로 분석할 수 없었음
- 단순 시각화 수준에서 벗어나기 위해 similarity 분석 필요

---

# ⚙️ What I Did (무엇을 했는가)

- [ ] 기능 구현 / 분석 내용
- [ ] 추가한 로직
- [ ] 변경한 구조

예)
- cosine similarity 기반 유전자 유사도 계산 구현
- 세포 간 거리 기반 pair 생성 로직 추가
- 분석 notebook → src 코드로 일부 분리

---

# 📊 Result (결과 / 변화)

- 무엇이 달라졌는가
- 수치 / 시각화 / 성능 변화

예)
- spatially 가까운 세포가 유전자적으로도 유사한 경향 확인
- 특정 클러스터에서 높은 상관관계 관측
- 분석 결과를 시각적으로 확인 가능

---

# 💡 Insight (배운 점 / 인사이트)

- 이번 작업에서 얻은 깨달음
- 예상과 달랐던 점
- 다음 단계로 이어질 생각

예)
- 단순 거리 기반 접근만으로는 interaction 설명에 한계 존재
- graph 구조로 확장 필요성 확인

---

# 🔄 Next Step (다음 단계)

- 이어서 할 작업

예)
- graph 생성 후 GNN 적용
- feature engineering 고도화

---

# 🧪 How to Test (실행 방법)

```bash
# 실행 방법
python notebooks/02_similarity.ipynb
