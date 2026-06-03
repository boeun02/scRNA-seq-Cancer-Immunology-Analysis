# scRNA-seq Cancer Immunology Analysis

암/면역 단일세포 RNA 시퀀싱 데이터 분석 파이프라인 구축 및 Tumor Microenvironment 연구 프로젝트


---

## Research Question
> **Phase 1**  
> "GEO 공개 데이터(GSE127465)를 직접 전처리해서 폐암 tumor-infiltrating immune cell을 UMAP으로 시각화하고 세포 타입을 annotation할 수 있는가?"

> **Phase 2**  
> "폐암 환자 TME에서 TAM은 기원에 따라 C1QC+ / SPP1+ 서브타입으로 분류되며, 이 패턴은 pan-cancer 수준에서 재현되는가?"
> 

> **Phase 3**  
> "폐암 TME에서 SPP1+ TAM이 높은 환자군은 면역치료 비반응군과 겹치는가? — scRNA-seq + H&E 이미지 공간 분포로 검증"

---s

## Background
- Single-cell RNA sequencing(scRNA-seq)은 개별 세포 수준에서 유전자 발현을 측정한다.
- Tumor Microenvironment(TME)는 암세포와 면역세포, 기질세포가 공존하는 복잡한 생태계로, 면역치료 반응의 핵심 결정 인자로 주목받고 있다.
- 기존 연구는 bulk RNA-seq 중심이었으나, scRNA-seq을 통해 세포 타입별 이질성(heterogeneity)을 분해하면 치료 반응 예측에 새로운 관점을 제공할 수 있다.


---

## Paper Reproduction (Phase 2)

> Nguyen TDT, Lee AJ, Park HJ, et al.  
> **Pan-Cancer Single-Cell RNA Sequencing Analysis Refines Multi-Origin Monocyte and Macrophage Lineages**  
> *Cancer Immunol Res* 2026;14:350–66  
> Corresponding authors: Inkyung Jung (KAIST), Woong-Yang Park (Samsung Medical Center)

- Pan-cancer macrophage lineage 분류 파이프라인 재현
- GSE127465 폐암 데이터 기반으로 분석 적용 후 GSE154763 다암종 데이터로 독립 검증

### 재현 결과 (Phase 2a — GSE127465 폐암)
 
| 서브타입 | 논문 marker (5개) | 내 DEG top 50 overlap | 일치율 |
|---|---|---|---|
| C1QC+ TAM | C1QA, C1QB, C1QC, APOE, FOLR2 | C1QA, C1QB, C1QC, APOE, FOLR2 | **5/5 (100%)** |
| SPP1+ TAM | SPP1, GPNMB, CTSD, MRC1, CD63 | SPP1, GPNMB, CTSD, MRC1, CD63 | **5/5 (100%)** |
 
> GSE127465 폐암 단일 데이터에서 논문의 pan-cancer TAM 서브타입 패턴이 동일하게 재현됨
> ISG15+ TAM은 단일 암종 데이터의 한계로 뚜렷한 클러스터로 분리되지 않음 -> phase 2b 다암종 확장에서 검증

### 독립 검증 결과 (Phase 2b — GSE154763, 8개 암종)
 
**암종별 TAM subtype 구성 비율 (%):**
 
| 암종 | C1QC+ | SPP1+ | ISG15+ | Other |
|---|---|---|---|---|
| ESCA | 22.8 | 0.0 | 0.0 | 77.2 |
| KIDNEY | 17.5 | 0.0 | 0.0 | 82.5 |
| LYM | 9.9 | 0.0 | 90.1 | 0.0 |
| MYE | 86.9 | 0.0 | 0.0 | 13.1 |
| OV-FTC | 58.7 | 41.3 | 0.0 | 0.0 |
| PAAD | 74.2 | 25.8 | 0.0 | 0.0 |
| THCA | 13.3 | 15.0 | 4.3 | 67.4 |
| UCEC | 20.6 | 25.6 | 7.6 | 46.2 |

**UpSet Plot 주요 결과**
- C1QC+ TAM - 8개 암종 전부 존재 (보편적 패턴)
- SPP1+ TAM - 4개 암종에만 존재 (OV-FTC, PAAD, THCA, UCEC)
- ISG15+ TAM - 3개 암종에만 존재 (LYM 90.1%, THCA, UCEC)
- **Phase 2a 한계였던 ISG15+ TAM이 다암종 확장에서 확인됨** -> 단일 암종 데이터의 한계 검증 완료

![TAM Subtype Composition by Cancer Type](docs/figures/phase2b_TAM_composition.png)
![UpSet Plot](docs/figures/phase2b_upset_plot.png)

---

## Methodology

```
GEO 공개 데이터 다운로드 (폐암 tumor-infiltrating immune cells)
       ↓
QC → Normalization → HVG 선택 → PCA → UMAP → Clustering
       ↓
세포 타입 annotation (Marker gene 기반)
       ↓
TAM 서브타입 세분화 (C1QC+, SPP1+) + DEG 분석 (Wilcoxon)
       ↓
논문 marker gene vs DEG top 50 overlap 검증
       ↓
TME 새포 구성 분석 (샘플별 / 암종별 TAM 비율)
       ↓
다암종 확장 (GSE154763, 8개 암종) — 독립 검증
       ↓
UpSet plot — 암종별 TAM subtype 조합 패턴 시각화
       ↓
결과 시각화 (UMAP, dotplot, heatmap, violin plot)
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
│   ├── data/
│   │   └── pbmc3k_raw.h5ad
│   └── 01_pbmc_tutorial.ipynb           ← Scanpy 기초 파이프라인 실습
├── phase1_scrna/
│   ├── dataset/
│   │   ├── GSE127465_gene_names_human_41861.tsv
│   │   └── GSE127465_RAW/               ← raw tsv 파일들
│   └── 01_geo_pipeline.ipynb            ← GEO 실데이터 전처리 파이프라인
├── phase2_analysis/
├── phase2_analysis/
│   ├── 01_myeloid_subset.ipynb       ← 골수계 서브셋팅 + TAM annotation (2a)
│   ├── 02_DEG_analysis.ipynb         ← DEG + overlap 확인 + dotplot (2a) + 다암종 DEG (2b)
│   └── 03_TME_composition.ipynb      ← TME 구성 분석 (2a + 2b)
└── phase3_project/
    ├── 01_preprocessing.ipynb
    ├── 02_clustering_annotation.ipynb
    ├── 03_TAM_treatment_response.ipynb
    ├── 04_HE_image_analysis.ipynb       ← DINOv2 feature 추출
    ├── 05_integration_visualization.ipynb
    ├── src/
    │   ├── preprocess.py
    │   ├── clustering.py
    │   ├── annotation.py
    │   ├── visualization.py
    │   └── image_features.py            ← DINOv2 feature 추출
    └── results/
        └── figures/
```
---

## Data
이 프로젝트는 GEO 공개 데이터를 사용합니다.

| 소스 | 데이터셋 | 내용 | Phase |
|------|----------|------|-------|
| GEO (NCBI) | GSE127465 | 폐암 tumor-infiltrating immune cells scRNA-seq | Phase 1~2a |
| GEO (NCBI) | GSE154763 | 8개 암종 골수계 세포 pan-cancer atlas (Set 1) | Phase 2b |
| GEO (NCBI) | GSE131907 | 폐선암 LUAD (~208k cells) | Phase 2b 예정 |
| GEO (NCBI) | GSE122960 | 정상 폐 (Healthy lung) | Phase 2b 예정 |

## GSE127465 다운로드 방법
1. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127465 접속
2. 아래 파일 다운로드:
   - GSE127465_RAW.tar
3. 압축 풀고 phase1_scrna/dataset/ 폴더에 위치


---

## Study Log
| Phase | 기간 | 내용 | 상태 |
|-------|------|------|------|
| Phase 0 | 2026.04.21 ~ 2026.04.28 | 환경 세팅 + Scanpy 기초 | ✅ 완료 |
| Phase 1 | 2026.04.30 ~ 2026.05.10 | GEO 실데이터 scRNA-seq 파이프라인 (GSE127465 폐암) | ✅ 완료 |
| Phase 2a | 2026.05.16 ~ 2026.05.22 | TAM 서브타입 annotation + DEG 분석 + 논문 재현 | ✅ 완료 |
| Phase 2b | 2026.05.23 ~ 2026.06.01 | 다암종 확장 — GSE154763, GSE131907 통합 검증 | 🔄 진행중 |
| Phase 3 | 2026.12~ | 메인 프로젝트 — scRNA-seq × H&E 이미지 통합 분석 | ⏳ 예정 |

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

## Tech Stack

- Python — Scanpy, Harmony, pandas, matplotlib, seaborn, upsetplot
- Jupyter Notebook

---

## Environment

```bash
conda env create -f environment.yml
conda activate spatial
```

패키지 상세 내역: [docs/environment.md](docs/environment.md)

본 분석은 Windows 환경에서 재현성을 확인하였다.
PCA, UMAP, Leiden 단계에는 'random_state = 42'를 지정했으나, OS 및 패키지 버전 차이에 따라 결과가 일부 달라질 수 있다.
동일 환경 내 재실행 시 결과가 일관적으로 재현되는지를 기준으로 삼았다.

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

---

## Notes
- 바이오 용어 단어장: See [docs/bio_keywordbooks.md](docs/bio_keywordbooks.md)
