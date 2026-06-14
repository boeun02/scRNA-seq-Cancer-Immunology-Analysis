<26.04.25 ~ 26.04.30>
# Scanpy tutorial

## 1. Basic
### 1. Preprocessing and clustering
1. bone marrow mononuclear cells: 골수 단핵세포
2. measured: 측정 된
3. 10X Multiome Gene Expression: (회사 제품 이름) 멀티옴 -> 하나의 세포에서 동시에 두가지 정보를 측정하는 기술
4. Gene Expression: 유전자 발현
5. Chromatin Accessibility: 크로마틴 접근성 -> DNA가 얼마나 열려있는지 측정하는 것
6. count matrix: 카운트 행렬 (세포x유전자 형태의 숫자 표로 각 유전자가 몇번 발현되었는지 담긴 표)
7. specific gene population: 특정 유전자 집단
8. a scatter plot: 산점도 -> 2개의 연속형 변수 간의 관계를 데카르트 좌표계에 점으로 표현하여, 데이터의 추세, 상관관계, 이상치(Outlier)를 시각적으로 파악하는 그래프
9. transcriptomes: 전사체
10. log1p: log plus one
11. Logarithmize: 로그 변환
Anndata 구조
12. obs (Observations): 세포(Cell) 정보 (예: 어느 샘플에서 왔는지, QC 지표 등)
13. var (Variables): 유전자(Gene) 정보 (예: 미토콘드리아 유전자 여부 등)
14. X: 실제 발현량 데이터
15. PC = Principal Component (주성분)
    단수: PC
    복수: PCs
16. scanpy 함수에서 tl, pl, pp의 의미
    - pp: preprocess - 전처리 관련 함수 (데이터 준비)
        - normalize
        - filter
        - scale
        - neighbors
        - highly_variable_genes
    - tl: tool - 실제 분석 알고리즘 (분석 수행)
        - pca
        - umap
        - leiden
        - rank_genes_groups
    - pl: plotting - 시각화 함수 (결과 시각화)
        - violin
        - umap
        - dotplot
        - heatmap
    + get: 결과 추출


# PHASE 1

## Data Structure
### 1. AnnData

<26.05.02 ~ ...>
# PHASE 1

## GEO pipeline
### 1. Raw Data 불러와서 데이터 구조 확인하기
데이터 구조
- 행 = 세포 (barcode)
- 열: 유전자 (gene_name)
- 값: raw_count (int형 값)
    - AnnData 구조
        AnnData
        ├─ X        : 메인 행렬, cell × gene expression matrix
        ├─ obs      : cell metadata table
        ├─ var      : gene metadata table
        ├─ uns      : unstructured data, 전역 설정/결과 저장소
        ├─ obsm     : cell 기준의 다차원 matrix 저장소
        ├─ varm     : gene 기준의 다차원 matrix 저장소
        ├─ layers   : X와 같은 shape의 보조 expression matrix
        └─ obsp     : cell × cell pairwise matrix
        
        - obs : 세포별 정보 tb
            즉, adata.obs의 행 개수는 adata.n_obs와 같다
            > obs는 DB로 따지면 cell TB임
        - var: 유전자별 정보 테이블
            > DB로 치면 gene TB
        - X: 핵심 expression matrix
            > DB로 치면 X는 cell_id, gene_id, expression_value 등을 가진 매핑 테이블/관계 테이블에 가깝다
        - layers: X와 같은 모양의 보조 행렬
            adata.X : 보통 normalize/log1p 된 값
            adata.layers['counts']: 원본 raw count
            > 즉, 둘 다 shape는 같다
            내 데이터로 따지면 counts layer가 있으니까 원본 count를 따로 보존 해둔 상태
        - obsm: observation matrix = 세포별 다차원 좌표/임베딩 저장소
            > obs는 1차원 컬럼 위주고 obsm은 각 세포마다 벡터/행렬 형태의 결과 저장
        - varm: var의 다차원 버전
        - uns: unstructured annoation = 특정 cell이나 gene행에 딱 맞춰지는 데이터가 아닌 전역 결과/설정/메타정보 저장소
            > uns['neighbors']에는 neighbor graph를 만들때 사용한 정보가 들어가고 실제 cell-cell 연결 행렬은 obsp에 들어감
        - obsp: observation pairwise = cell x cell

### 2. Sparse Matrix
- Dense Tensor: 배열의 모든 위치에 값을 가지는 텐서
    - 배열 안에 0과 같이 생략 가능한 원소까지 모두 저장하여 텐서의 크기가 늘어남
    - 텐서 크기에 비례해서 메모리를 사용하기 때문에 OOM(out of memory)문제가 발생
    - 데이터의 크기가 커질수록 계산량과 계산 시간을 증가하게 함
- Sparse Tensor: 0이 아닌 원소와 그 위치를 저장하는 텐서
    - 텐서에 0이 많을 수록 저장하는 양이 줄어들어 효율적인 memory사용이 가능하면 계산 시간이 감소하게 된다
    1. COO(Coorfinate list) 방식
    2. CSR/CSC(Compressed Sparse Row/Column) 방식

### 3. COO, CSR / CSC
1. COO(Coorfinate list) 방식
    - 행, 열, 데이터의 인덱스 순서 배열을 활용하여 값의 위치를 저장하는 방식
    - 매우 직관적인 방식이지만 행과 열의 인덱스를 별도로 저장
    - 같은 행 혹은 같은 열에 데이터가 많을 경우, 반복해서 같은 값(row 1)이 저장되어 메모리를 비효율적으로 사용
    - 데이터, 원소에 접근할 때 마다 행과 열의 인덱스 값을 조회하므로 연산 성능 저하 가능성 있음
2. CSR/CSC(Compressed Sparse Row/Column) 방식
    - '행/열의 경계를 표시하는 배열 row/column index pointer'와 '행과 열의 원소 순서대로 인덱스를 정렬한 배열 row/column index'을 활용하여 텐서의 원소를 저장
    - 원소를 순회하는 방식으로 접근할 수 있어 효율적인 메모리 사용이 가능하지만, 구조가 복잡하고 직관적이지 않음

### 4. 그 외
- barcode sequence:
    barcode는 세포 하나하나를 구별하는 짧은 DNA 서열
    sequence는 생물학에서 순서가 아니라 DNA 염기 서열을 뜻함 (ex- bcIHWD 이런게 ATCG로 이루어진 짧은 DNA서열인데 표기할 때 압축하여 표현하면 저렇게 표현 됨)

    즉, scRNA-seq 실험할 때 세포 하나씩 캡슐에 넣고 거기에 고유한 DNA 태그(barcode)를 붙여서 '이 유전자 발현 데이터는 이 세포의 것' 이라고 표시하는 것.
    
    근데 이때 바코드는 샘플(각각의 tsv파일)마다 독립적으로 생성 되니까 p1환자 샘플과 p2 환자 샘플에서 같은 barcode가 나올 수 있다 (한 스키마 당 고유키 하나씩 할당한다고 치면 완전히 다른 스키마에서는 같을 수도 있다는 것.)

    -> 그래서 여러 샘플들을 한 파일로 합칠 때 중복 문제가 발생

- numpy와 pandas에서 행렬 전치 시키기:
    transpose의 약어인 .T를 붙여주며 행이 열이되고 열이 행이 됨

    scRNA-seq에서는 AnnData가 항상 행=세포, 열=유전자 구조를 요구함
    원본 데이터가 행=유전자, 열=세포로 저장된 경우 .T로 전치 필요
        -> 데이터마다 다르므로 로딩 전 반드시 구조를 print 찍어서 확인할 것
    ex. adata = sc.AnnData(sp.csr_matrix(df.T.values.astype('float32')))


## Preprocessing
### 1. QC
### 2. MAD
### 3. Doublelet



bioinformatics-concepts.md

├─ Data Structure
│  ├─ Sparse Matrix
│  ├─ CSR / CSC
│  ├─ AnnData
│
├─ Preprocessing
│  ├─ QC
│  ├─ MAD
│  ├─ Doublet
│  ├─ Ambient RNA
│
├─ Normalization
│  ├─ CPM
│  ├─ log1p
│
├─ Feature Selection
│  ├─ HVG
│
├─ Dimensionality Reduction
│  ├─ PCA
│  ├─ Elbow Point
│  ├─ Embedding
│
├─ Clustering
│  ├─ Neighbors Graph
│  ├─ Leiden
│  ├─ Resolution
│
├─ Batch Correction
│  ├─ Batch Effect
│  ├─ Harmony
│
├─ Annotation
│  ├─ Marker Gene
│  ├─ Cell Type Annotation
│
├─ Differential Expression
│  ├─ DEG
│  ├─ logFC
│  ├─ p-value
│  ├─ adjusted p-value
│
├─ Immunology
│  ├─ TAM
│  ├─ C1QC TAM
│  ├─ SPP1 TAM
│  ├─ TME
│
└─ Future
   ├─ CellChat
   ├─ Trajectory
   ├─ GSVA
   ├─ Pseudobulk



LYM_META column description

- index
  각 cell의 barcode 또는 cell ID.
  예: AACACGTGTTTGGGCC-15

- batch
  batch 번호.
  샘플 처리 단위, sequencing batch, 또는 데이터 병합 과정에서 부여된 batch ID로 보임.

- patient
  환자 ID.
  예: P20181123

- tissue
  조직 출처.
  현재 값은 T이며, tumor tissue를 의미하는 것으로 보임.

- percent_hsp
  heat shock protein 관련 gene expression 비율로 추정.
  세포 스트레스 상태를 평가하는 QC 지표로 사용될 수 있음.

- percent_mito
  mitochondrial gene expression 비율.
  일반적으로 세포 품질 QC에 사용됨. 값이 높으면 damaged/dead cell 가능성을 의심할 수 있음.

- n_genes
  해당 cell에서 검출된 gene 수.
  single-cell QC에서 cell complexity를 나타내는 지표.

- n_counts
  해당 cell의 total UMI/count 수.
  sequencing depth 또는 library size를 나타내는 지표.

- MajorCluster
  이미 부여된 cell type/subtype annotation.
  예: M06_Macro_ISG15, M07_Macro_C1QC, M04_Mono_CD14.
  이번 분석에서는 macrophage cluster 추출과 subtype 재검증의 기준 컬럼으로 사용 가능.

- source
  데이터 제공 출처 또는 연구 그룹.
  예: ZhangLab.

- tech
  사용된 scRNA-seq 플랫폼 또는 library preparation 방식.
  예: 10X5. 10x Genomics 5' 기반 데이터로 보임.

- cancer
  암종 정보.
  현재 값은 LYM이며 lymphoma를 의미.

- UMAP1
  기존 분석에서 계산된 UMAP 1번 좌표.

- UMAP2
  기존 분석에서 계산된 UMAP 2번 좌표.


  Other macrophage 구성 해석
| MajorCluster    | n_cells | percent_in_other | 해석 방향                                           |
| --------------- | ------: | ---------------: | ----------------------------------------------- |
| M08_Macro_NLRP3 |    3903 |           25.48% | inflammatory / inflammasome-like macrophage     |
| M09_Macro_IL1B  |    2363 |           15.43% | inflammatory cytokine macrophage                |
| M10_Macro_GPNMB |    2264 |           14.78% | SPP1-like 또는 lipid/remodeling TAM 후보            |
| M12_Macro_LYVE1 |    2202 |           14.38% | resident-like / tissue macrophage 계열 가능         |
| M08_Macro_FN1   |    1319 |            8.61% | matrix remodeling / fibro-inflammatory state 가능 |
| M11_Macro_LYVE1 |    1217 |            7.95% | resident-like / tissue macrophage 계열 가능         |
| M13_Macro_INHBA |    1100 |            7.18% | TGFβ/activin 관련 activated macrophage 가능         |
| M09_Macro_INHBA |     947 |            6.18% | activated / immunoregulatory macrophage 가능      |

