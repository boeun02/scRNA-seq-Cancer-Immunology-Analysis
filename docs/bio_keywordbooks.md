<26.04.25>
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