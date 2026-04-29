# scRNA-seq Cancer Immunology Analysis

암/면역 단일세포 RNA 시퀀싱 데이터 분석 파이프라인 구축 및 Tumor Microenvironment 연구 프로젝트
> 분석 파이프라인을 모듈화하여 데이터셋 교체 시 파라미터 설정만으로 재실행 가능하도록 설계


---

## Research Question

> "폐암 환자의 Tumor Microenvironment에서 면역세포 구성은 치료 반응과 어떤 관계가 있는가?"


---

## Background
- Single-cell RNA sequencing(scRNA-seq)은 개별 세포 수준에서 유전자 발현을 측정한다.
- Tumor Microenvironment(TME)는 암세포와 면역세포, 기질세포가 공존하는 복잡한 생태계로, 면역치료 반응의 핵심 결정 인자로 주목받고 있다.
- 기존 연구는 bulk RNA-seq 중심이었으나, scRNA-seq을 통해 세포 타입별 이질성(heterogeneity)을 분해하면 치료 반응 예측에 새로운 관점을 제공할 수 있다.


---

## Methodology

```
GEO 공개 데이터 다운로드 (폐암 tumor-infiltrating immune cells)
       ↓
QC → Normalization → HVG 선택 → PCA → UMAP → Clustering
       ↓
세포 타입 annotation (Marker gene 기반)
       ↓
Tumor Microenvironment 세포 구성 분석
       ↓
DEG 분석 → 치료 반응 연관 유전자 탐색
       ↓
결과 시각화 (UMAP, heatmap, violin plot, dot plot)
       ↓
생물학적 해석: 어떤 면역세포 구성이 치료 반응과 연관되는가
```


---

## Project Structure

```
scrna-cancer-immunology/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── bio_keywordbooks.md              ← 용어정리
│   └── environment.md
├── phase0_basics/
│   ├── data
│   │   └── pbmc3k_raw.h5ad
│   └── 01_pbmc_tutorial.ipynb           ← Scanpy 기초 파이프라인 실습
├── phase1_scrna/
│   ├── dataset
│   │   ├── GSE127465_gene_names_human_41861.tsv
│   │   ├── human_cell_metadata_54773x25.tsv
│   │   └── GSE127465_human_counts_normalized_54773x41861.mtx
│   └── 01_geo_pipeline.ipynb            ← GEO 실데이터 전처리 파이프라인
├── phase2_analysis/
│   ├── 01_DEG_analysis.ipynb            ← 차등발현유전자 분석
│   ├── 02_TME_composition.ipynb         ← TME 세포 구성 분석
│   └── 03_paper_reproduction.ipynb      ← 논문 재현
└── phase3_project/
    ├── 01_preprocessing.ipynb
    ├── 02_clustering_annotation.ipynb
    ├── 03_TME_analysis.ipynb
    ├── 04_DEG_visualization.ipynb
    ├── src/
    │   ├── preprocess.py      ← QC, normalization 함수화
    │   ├── clustering.py      ← UMAP, leiden 파라미터 관리
    │   ├── annotation.py      ← marker gene 기반 annotation 자동화
    │   └── visualization.py   ← 시각화 함수 모음
    └── results/
        └── figures/
```


---

## Pipeline Design

분석 파이프라인은 `src/` 모듈로 분리되어 있어 데이터셋 교체 시 파라미터 설정만으로 재실행 가능

```python
from src.preprocess import run_qc, normalize
from src.clustering import run_umap, run_leiden
from src.annotation import annotate_celltypes
from src.visualization import plot_umap, plot_heatmap

# 데이터셋만 바꾸면 전체 파이프라인 재실행 가능
adata = run_qc(data_path="data/GSE127465")
adata = normalize(adata)
adata = run_umap(adata, n_pcs=30, resolution=0.5)
adata = annotate_celltypes(adata, marker_genes=LUNG_MARKERS)
plot_umap(adata, color="cell_type", save="results/figures/umap.png")
```


---

## Study Log
| Phase | 기간 | 내용 | 상태 |
|-------|------|------|------|
| Phase 0 | 2026.04.21 ~ 2026.04.28 | 환경 세팅 + Scanpy 기초 | ✅ 완료 |
| Phase 1 | 2026.04.30 ~ | GEO 실데이터 scRNA-seq 파이프라인 (GSE127465 폐암) | 🔄 진행중 |
| Phase 2 | 2026.09~ | DEG 분석 + TME 구성 분석 + 논문 재현 | ⏳ 예정 |
| Phase 3 | 2026.12~ | 메인 프로젝트 — TME 면역세포 구성 vs 치료 반응 분석 | ⏳ 예정 |


---

## Data
이 프로젝트는 GEO 공개 데이터를 사용합니다.

| 소스 | 데이터셋 | 내용 |
|-------|------|------|
| GEO (NCBI) | GSE127465 | 폐암 tumor-infiltrating immune cells scRNA-seq |

## 다운로드 방법
1. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127465 접속
2. 아래 세 파일 다운로드:
   - GSE127465_human_counts_normalized_54773x41861.mtx.gz
   - GSE127465_gene_names_human_41861.tsv.gz
   - GSE127465_human_cell_metadata_54773x25.tsv.gz
3. 압축 풀고 phase1_scrna/dataset/ 폴더에 위치

---

## Tech Stack

- Python — Scanpy, Harmony, pandas, matplotlib, seaborn
- R — Seurat, DESeq2 (Phase 2~3)
- Jupyter Notebook


---

## Notes
- 바이오 용어 단어장: See [docs/bio_keywordbooks.md](docs/bio_keywordbooks.md)


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

