# Environment Setup

## Python Version
- Python 3.10

---

## Environment (Conda)

```bash
# 환경 생성
conda env create -f environment.yml

# 환경 활성화
conda activate spatial
```

---

## environment.yml

```yaml
name: spatial
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - python=3.10
  - harmonypy
  - pip
  - pip:
    - scanpy
    - scipy
    - numpy
    - pandas
    - scikit-misc
    - anndata
    - umap-learn
    - leidenalg
    - igraph
    - matplotlib
    - seaborn
    - scikit-learn
    - scikit-image
    - statsmodels
    - numba
    - h5py
    - tqdm
    - pynndescent
    - session-info2
```

---

## 패키지 역할

| 패키지 | 역할 |
|--------|------|
| scanpy | scRNA-seq 분석 핵심 라이브러리 |
| anndata | scRNA-seq 데이터 구조 (AnnData 객체) |
| harmonypy | 배치 보정 (샘플 간 기술적 편차 제거) |
| umap-learn | UMAP 차원 축소 |
| leidenalg | Leiden 클러스터링 알고리즘 |
| igraph | 그래프 기반 클러스터링 지원 |
| pynndescent | KNN 그래프 생성 (UMAP 전처리) |
| scikit-misc | HVG 선택 (seurat_v3 방식) |
| numba | 연산 가속 |
| scipy / numpy | 수치 연산 |
| pandas | 데이터프레임 처리 |
| matplotlib / seaborn | 시각화 |
| scikit-learn | 머신러닝 유틸리티 |
| scikit-image | 이미지 처리 (Phase 3) |
| statsmodels | 통계 분석 |
| h5py | h5ad 파일 입출력 |
| tqdm | 진행률 표시 |
| session-info2 | 분석 환경 버전 기록 |