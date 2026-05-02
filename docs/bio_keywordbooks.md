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

<26.05.02 ~ ...>
# PHASE 1

## GEO pipeline
### 1. Raw Data 불러와서 데이터 구조 확인하기
데이터 구조
- 행 = 세포 (barcode)
- 열: 유전자 (gene_name)
- 값: raw_count (int형 값)

- barcode sequence:
    barcode는 세포 하나하나를 구별하는 짧은 DNA 서열
    sequence는 생물학에서 순서가 아니라 DNA 염기 서열을 뜻함 (ex- bcIHWD 이런게 ATCG로 이루어진 짧은 DNA서열인데 표기할 때 압축하여 표현하면 저렇게 표현 됨)

    즉, scRNA-seq 실험할 때 세포 하나씩 캡슐에 넣고 거기에 고유한 DNA 태그(barcode)를 붙여서 '이 유전자 발현 데이터는 이 세포의 것' 이라고 표시하는 것.
    
    근데 이때 바코드는 샘플(각각의 tsv파일)마다 독립적으로 생성 되니까 p1환자 샘플과 p2 환자 샘플에서 같은 barcode가 나올 수 있다 (한 스키마 당 고유키 하나씩 할당한다고 치면 완전히 다른 스키마에서는 같을 수도 있다는 것.)

    -> 그래서 여러 샘플들을 한 파일로 합칠 때 중복 문제가 발생

- numpy와 pandas에서 행렬 전치 시키기:
    transpose의 약어인 .T를 붙여주며 행이 열이되고 열이 행이 됨
    ex. adata = sc.AnnData(sp.csr_matrix(df.T.values.astype('float32')))