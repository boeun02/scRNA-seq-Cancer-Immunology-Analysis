# spatial-transcriptomics

H&E 이미지의 형태학적 특징과 유전자 발현의 관계를 분석하는 연구 프로젝트

---

## Research Question

> "공간적으로 가까운 spot은 조직 형태와 유전자 발현에서 동시에 유사한가?"

---

## Background
- Spatial Transcriptomics는 조직 내 세포의 위치 정보와 유전자 발현을 동시에 측정한다.
- 기존 연구는 유전자 발현 데이터 중심이었으나, H&E 이미지의 형태학적 정보를 결합하면 조직 구조와 유전자 발현의 관계를 새로운 관점에서 해석할 수 있다.

---

## Methodology

```
Visium H&E 이미지
↓
spot 위치 기준 패치 단위 crop
↓
pretrained DINOv2로 형태학적 특징 추출
↓
같은 spot의 유전자 발현 벡터와 매핑
↓
공간 거리 / 형태 유사도 / 유전자 유사도 관계 분석
```

---
## Project Structure

```

spatial-transcriptomics-study/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── environment.md
├── phase0_basics/
│   └── 01_pbmc_tutorial.ipynb
├── phase1_scrna/
│   └── 01_geo_pipeline.ipynb
├── phase2_spatial/
│   ├── 01_visium_eda.ipynb
│   └── 02_paper_reproduction.ipynb
└── phase3_project/
    ├── 01_patch_extraction.ipynb
    ├── 02_feature_extraction.ipynb
    ├── 03_alignment_analysis.ipynb
    ├── src/
    │   ├── patch_extractor.py
    │   └── feature_aligner.py
    └── results/
        └── figures/

```

---

## Study Log
| Phase | 기간 | 내용 | 상태 |
|-------|------|------|------|
| Phase 0 | 2026.04~ | 환경 세팅 + Scanpy 기초 | 🔄 진행중 |
| Phase 1 | 2026.06~ | scRNA-seq 파이프라인 | ⏳ 예정 |
| Phase 2 | 2026.09~ | Spatial 데이터 + 논문 재현 | ⏳ 예정 |
| Phase 3 | 2026.12~ | 차별화 프로젝트 | ⏳ 예정 |

---

## Notes
- 바이오 용어 단어장: [notion 링크 추후 추가 예정]

---

## Tech Stack

- Python (Scanpy, Squidpy)
- PyTorch (DINOv2)
- Jupyter Notebook

---

## Environment
See [docs/environment.md](docs/environment.md)

---

## Branch Strategy

| 브랜치 | 역할 |
|--------|------|
| main   | 최종 결과 |
| dev    | 개발 브랜치 |
| feature/* | 기능/실험 단위 |

---

## Commit Convention

| 타입 | 설명 |
|------|------|
| feat | 기능 추가 |
| analysis | 데이터 분석 |
| fix | 버그 수정 |
| refactor | 코드 개선 |
| wip | 실험 중 |

