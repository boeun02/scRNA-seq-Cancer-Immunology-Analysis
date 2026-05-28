# Phase 1

**목표:** 튜토리얼 데이터 말고 날 것의 GEO 데이터를 혼자 전처리해서 UMAP까지 그릴 수 있는 수준. 이게 Phase 2 진입 조건.

# 0. GEO에서 scRNA-seq 공개데이터 다운로드

GEO (NCBI Gene Expression Omnibus)에서 암 관련 scRNA-seq 공개 데이터 1개 직접 다운로드

- 폐암 데이터로 셀렉
**GSE127465** — 폐암 환자 tumor-infiltrating immune cells scRNA-seq

데이터 찾는 법> 참고 url: https://avocadaon.tistory.com/29

1. 구글에 GEO검색
2. GEO들어가서 우측 상단 네모 쳐둔 곳(검색창)에 원하는 데이터 검색
    - 나는 미리 주제를 정해둬서 찾아 놓은 accession number로 검색했는데 그냥 데이터 이름 쳐도 됨
        
        ex) breast cancer
        
        https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127465
        
        ![image.png](attachment:b16fd7de-b8bb-4c55-a880-1f9ce3f84741:image.png)
        
3. 스크롤 내려서 해당 실험의 platform 정보(GPL), sample정보(GSM) 링크도 클릭하여 확인
    
    ![image.png](attachment:98d8fb4a-96d4-4af7-8821-42c46228e59e:image.png)
    
4. 페이지 최하단 download 버튼 눌러 데이터 받을 수 있음
    
    ![image.png](attachment:cf8b9eb3-2297-45b4-9c06-f88dd904a357:image.png)
    
5. 나는 그 중에서 요거 세개 받겠음
    
    
    | 파일 | 역할 |
    | --- | --- |
    | ~~GSE127465_human_counts_normalized_54773x41861.mtx.gz~~
    GSE127465_RAW.tar → 로 변경 | 발현량 행렬 (X) |
    | ~~GSE127465_gene_names_human_41861.tsv.gz~~ | 유전자 이름 (var) |
    | ~~GSE127465_human_cell_metadata_54773x25.tsv.gz~~ | 세포 메타데이터 (obs) |
    
    이미 전처리가 다 된 데이터인걸 확인해서 GSE127465_RAW.tar raw 데이터만 받아주었음
    
6. 해당 파일 압축 해제해서 프로젝트 파일로 가지고 오기
    
    이때 꼭 gitignore 설정 추가하기 → 데이터 파일 겁나 커서 깃헙에 안올라감
    
    애초에 데이터셋은 민감한거니까… 나는ignore파일 설정 잘못해서 올렸다가 캐시 삭제하고 난리침
    
7. *GSE127465_human_counts_normalized_54773x41861.mtx.gz 데이터는 이미 전처리 된 데이터라 삭제 조치하고 raw 데이터 다시 받음 - 26.05.01 커밋완료*
    
    <aside>
    💡
    
    #### 왜 raw data를 받아서 다시했나?
    
    1. raw count는 통계적 가정의 시작점 이기 때문이다
        
        이후 처리 될 정규화. hvg, deg 등등의 작업에서 raw data기반으로 시작해야하는데 이미 nomalized 된 데이터는 어떤 방식으로 정규화 되었는지 batch correnction이 되었는지 scaling했는지 등을 직접 데이터를 핸들링한게 아니라 모를 수 밖에 없음
        
        즉 무의미하다는 것임
        
    2. 직접 전처리를 하여 핸들링 감각을 키우고 싶었다
        
        데이터를 직접 뜯어보며 이 데이터에서는 이런식으로 처리를 해야겠다, 이 데이터는 이렇게 생겼구나 등을 판단하며 그냥 파이프라인을 따라 치는것이 아닌 데이터를 핸들링 해보는 것이 프로젝트의 목적이었기 때문에 raw data를 선택했다
        
    3. QC/normalization의 기준을 이해하고 싶었다
        
        1, 2번과 비슷한 맥락
        
    4. 전문가가 직접 핸들링하여 전처리 된 data와 내가 직접 보면서 전처리 해본 데이터를 비교해보고 싶었다
        
        그냥 가져다 쓰면 어떻게 핸들링 했는지 완벽한 블랙박스 이지만 내가 한번 해본 데이터는 다른 사람이 처리한 데이터를 봤을때 대충 예상이라는 건 해볼 수 있게 됨
        
        어떻게 이렇게했는지 완벽히는 몰라도 내거와 비교하면서, 조금씩 파라미터 값을 수정해보면서 여기서 이렇게했구나, 전처리 과정에 내가 쓰지않은 단계를 추가했구나 이건뭘까 내 값과 별반 다르지않네 혹은 이분은 여기에 가중치를 잡고 데이터를 남기셨구나 등을 파악 해볼 수 있을 것 같았다
        
    </aside>
    

*26.04.30 - 커밋 완료*

---

# 1. GEO 데이터를 불러오기

### 0. RAW DATA 불러와서 데이터 구조 확인 하기

```python
import pandas as pd

df = pd.read_csv('dataset/GSE127465_RAW/GSM3635280_human_p1t3_raw_counts.tsv.gz', sep='\t', index_col=0, compression='gzip')
print(df.shape)
print(df.head())
```

- 아무거나 한개의 파일을 불러와서 구조를 확인 해보았다.
    
    ![image.png](attachment:6ce5f84b-9589-4d9b-a907-b80f012a47d6:image.png)
    
- 데이터 구조
    - 행 = 세포(barcode)
    - 열 = 유전자 (gene names)
    - 값: raw_count (정수 값)

### 1. RAW DATA 합쳐주기

- 이제 RAW 데이터 파일에 들어있는 모든 샘플 tsv파일을 합쳐주어야 한다.
- 이때 우리는 **인간 임상 데이터**만 분석 할 예정이기 때문에 *human* 데이터끼리만 합쳐준다.
→ 메모리 낭비 때문에/데이터 적합성

```python
import scanpy as sc
import pandas as pd
import scipy.sparse as sp
import glob
from tqdm import tqdm # 프로세스 진행상황 보려고 progress bar 추가 한 것 (데이터와 무관)

files = glob.glob('dataset/GSE127465_RAW/*human*.tsv.gz')

adata_list = []
for f in tqdm(files):
    df = pd.read_csv(f, sep='\t', index_col=0, compression='gzip')
    
    # sparse 변환으로 메모리 절약
    adata = sc.AnnData(sp.csr_matrix(df.T.values.astype('float32')))
    adata.obs_names = df.columns.tolist()
    adata.var_names = df.index.tolist()
    
    adata_list.append(adata)
    del df  # df 즉시 해제

adata_raw = sc.concat(adata_list, join='outer')
print(adata_raw.shape)

# 최종 저장
adata_raw.write_h5ad('GSE127465_human_all.h5ad')
```

![image.png](attachment:fc57e561-fe51-4799-9186-4af8b287322a:image.png)

- 이슈 사항 - *메모리 에러 발생(RAM 32GB 환경)*
    1. 메모리 에러가 발생하여서 raw count 값을 int → float형으로 변환
    ** float형으로 변환 시 정밀도가 약간 낮아지긴 하나 scRNA-seq count 데이터에서는 문제가 없다*
    2.  sparse로 변환하여 0인 값을 즉시 압축 저장하게 설정 → 실제 값은 변하지 않음 (메모리만 최적화)
    
    ![image.png](attachment:926f9566-c775-4d4c-87a3-a5fcce8bb5d1:image.png)
    
- **다중 샘플 scRNA-seq 데이터 통합 시 주의 사항**
    1. barcord 중복 문제
        - 원인: 각 샘플이 독립적으로 sequencing 되기 때문에 서로 다른 샘플에서 동일한 barcode 시퀀스가 나올 수 있다
        - 해결: sc.concat(index_unique=’-’)로 샘플 명을 barcode에 붙여서 고유하게 만들어주기
        - ex) bcIHWD → bcIHWD-0 → bcIHWD-1
    2. 메모리 문제
        - 원인: 26개의 샘플 X 수천개의 세포 X 42861 유전자 → 대용량 데이터
        - 해결
            - scipy.sparse로 sparse matrix 변환
            - 파일 읽고 del df로 즉시 해제
            - concat 후 del adata_list 즉시 해제
        
        <aside>
        💡
        
        #### spares가 뭐고 그걸 왜 썼는가?
        
        1. 왜 쓴건가?
            
            scRNA-seq 데이터는 수만 개의 세포x수만 개의 유전자로 구성 된 거대 행렬임 이거를 일반적인 방식인 Dense로 로드하면 메모리 에러가 남
            
            데이터 특성 상 데이터의 상당 부분이 0(유전자 미검출) 이라는 점에 착안하여 0이 아닌 유효한 데이터만 저장하는 Sparse Matrix 형식을 사용했다
            
        2. 무손실 압축(Lossless Compression)
            
            0을 삭제하는 것이 아닌 기록되지 않은 위치의 값은 0이라고 약속하는 방식이기 때문에 데이터 유실이나 왜곡이 없다
            
        - **Dense (밀집)**: 모든 칸에 메모리 할당 (0까지 전부 기록)
        - **Sparse (희소)**: 유효한 값의 좌표(행, 열)와 값만 기록
        1. 주요 행렬 형식 비교
        
        | **형식** | **특징** | **용도** |
        | --- | --- | --- |
        | **COO (Coordinate)** | (행, 열, 값) 좌표를 단순 기록, 직관적 | 데이터 초기 생성/구축 시 |
        | **CSR (Compressed Sparse Row)** | 행(Row) 중심으로 압축, 계산 속도가 매우 빠름 | **데이터 분석 및 머신러닝 학습 (권장)** |
        | **CSC (Compressed Sparse Column)** | 열(Column) 중심으로 압축, 특정 유전자 추출에 유리 | 특정 열(Feature) 슬라이싱 작업 시 |
        </aside>
        

```python
import scanpy as sc
import pandas as pd
import scipy.sparse as sp
import glob
from tqdm import tqdm

files = glob.glob('dataset/raw/GSE127465_RAW/*human*.tsv.gz')

# 데이터 구조 확인 (최초 1회)
df_check = pd.read_csv(files[0], sep='\t', index_col=0, compression='gzip')
print('shape:', df_check.shape)
print('index(행):', df_check.index[:3].tolist())
print('columns(열):', df_check.columns[:3].tolist())
del df_check
'''
    만약, 행 -> 세포 / 열 -> 유전자 라면 밑에 adata에 대입해줄 때 df.values
        열 -> 세포 / 행 -> 유전자 (반대) 라면 밑에 adata에 대입해줄 때 df.T.values
    내가 불러온 데이터는 전치가 필요 없었음
'''

adata_list = []
for f in tqdm(files):
    df = pd.read_csv(f, sep='\t', index_col=0, compression='gzip')
    
    # sparse 변환으로 메모리 절약
    adata = sc.AnnData(sp.csr_matrix(df.values.astype('float32')))
    adata.obs_names = df.index.tolist()
    adata.var_names = df.columns.tolist()
    
    adata_list.append(adata)
    del df # 파일 하나 당 한개씩 할당 받은 df를 바로 해제 해줌

adata_raw = sc.concat(adata_list, join='outer', index_unique='-')
del adata_list
print(adata_raw.shape)

adata_raw.write_h5ad('GSE127465_human_all.h5ad')
```

- 데이터를 돌리기 전에 먼저 raw데이터가 어떤 형식으로 들어있는지 파악하는 것이 중요
    - T는 transpose의 약어로 행렬을 전치 시켜줌(행→ 열, 열→ 행 / 즉 행과 열을 뒤집음)
    - 만약 raw dataset을 print찍어 보았을 때, 컬럼(열)에 세포가 들어있고 인덱스(행)에 유전자가 들어있다면  이건 전치를 시켜줘야 함 → 그 반대라면 T를 안 붙여줘도 된다

![image.png](attachment:8552349e-0103-4f1e-9fd9-8743cb29c5b4:image.png)

*26.05.02 - 커밋 완료*

---

# 1. QC 진행

**AnnData 고정 속성 → 알아두자**

| 속성 | 의미 | 형태 |
| --- | --- | --- |
| adata.X | 발현량 행렬 | (세포 x 유전자) |
| adata.obs | 세포 메타데이터 | DataFrame, 행=세포 |
| adata.var | 유전자 메타데이터 | DataFrame, 행=유전자 |
| adata.obs_names | 세포 이름 (index) | 배열 |
| adata.var_names | 유전자 이름 (index) | 배열 |
| adata.obsm | 세포 임베딩 (PCA, UMAP 등) | dict |
| adata.layers | 추가 발현량 행렬 | dict |

adata.X는 main 테이블이라 생각하면 됨, 행은 세포 열은 유전자로 이루어진 main테이블

adata.obs와 adata.var는 metadata container라고 생각하면 됨 main테이블에 fk받아와서 생겨진 metadata들이 저장 된 테이블

<aside>
💡

#### anndata에 데이터 구조가 왜 row=cell, column=gene 인가?

scRNA의 기본 분석 단위가 “세포”이기 때문이다

세포 간 거리를 계산하고 세포를 클러스터링하고 세포를 임베딩하는 등 세포가 중심이기 때문에

행=observation=cell 인거고
열=feature=gene 인것이다

</aside>

## QC란?

- 전체 RAW Data를 전처리 하는 첫 단계로써, 이 전체 세포 데이터들 중에서 **죽거나 망가진 세포들만을 1차적으로 걸러내는 작업**

### 1. QC의 핵심 3가지 지표

- count depth (세포 당 총 count 수) = total_counts→ 너무 적으면 죽은 세포 / 너무 많으면 doublet
    - total counts가 QC 지표인 이유?
        
        세포가 살아있으면 활발하게 유전자를 발현, 근데 죽은 세포는 이미 RNA가 분해되거나 새어나간 상태라 잡히는 count 자체가 적어짐
        
        하지만 count가 너무 많아도 문제 → doublet 의심(세포 두 개가 합쳐진 것)
        
- 세포 당 발현 유전자 수 = n_genes_by_counts→ 너무 적으면 빈 droplet
- 미토콘드리아 유전자 비율 = pct_counts_mt→ 너무 높으면 죽어가는 세포
    - 왜 mt비율이 높으면 죽어가는 세포로 볼까?
        
        정상 세포는 에너지를 만들 때 미토콘드리아를 사용
        세포가 죽어가면 세포막이 터지면서 세포질 RNA는 모두 빠져나가고 mtRNA만 남게 됨
        그래서 mt 비율이 비정상적으로 높다면 ‘**이 세포는 망가진 것이구나**’ 하고 판단 하게 되는 것
        

이 세 가지를 같이 봐야 한다. **한 가지만 보면 오판 될 수 있음**

### 2. 주의 사항

- 고정 기준 값을 사용하지 말 것
- MAD(median absolute deviation) 기반 자동 필터링을 권장하고 5MAD를 기준으로 비교적 관대하게 필터링을 하는 것을 추천한다
    
    → 예를 들어 **mt비율이 높은 세포가 진짜 생물학적인 거라면?** 이런 상황이 발생할 수 있기 때문에
    
- mt count비율이 높은 세포는 호흡 과정에 관여하는 세포일 수 있어서 필터링 하면 안될 수도 있음
반면 count가 낮거나 높은 세포는 휴지기 세포 집단이거나 크기가 큰 세포일 수도 있음
그래서 **단일 지표로만 필터링 하는 것은 추천하지 않고 여러 지표를 함께 고려**하는 것이 제대로 된 QC방법이라고 할 수 있음
    - 단일 지표는 조건 하드코딩 같은 것 → 예를 들어 ‘20개 이하면 필터링’ << 이런 조건
- Ambient RNA 보정(SoupX)과 Doublet 감지(scDblFinder)도 QC의 일부인데 Doublet detection은 여러 배치가 합쳐진 데이터에서는 배치 별로 따로 실행해야 함

*참고 문서: https://www.sc-best-practices.org/preprocessing_visualization/quality_control.html*

## 0. 전체 RAW DATA 확인

```python
import scanpy as sc

adata = sc.read_h5ad('dataset/raw/GSE127465_human_all.h5ad')
print(adata)
```

![image.png](attachment:5e6c3db6-e2ce-45b2-9422-380d7071d2ec:image.png)

: 데이터가 제대로 들어온 것을 확인할 수 있다. 이제 본격적인 QC 진행을 해볼 것

## 1. QC 지표 시각화

```python
import scanpy as sc

#mt: 미토콘드리아 - 사람의 mt를 가져올거니까 MT-를 접두사로 하는 데이터 추출
#rebo는 리보솜. hb는 헤모글로빈
adata.var['mt'] = adata.var_names.str.startswith('MT-')
adata.var['ribo'] = adata.var_names.str.startswith(('RPS', 'RPL'))
adata.var['hb'] = adata.var_names.str.contains(r'^HB[ABDEGMQZ]\d*(?!\w)')
# pp는 preprcessing - 데이터 변환 및 계산
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt', 'ribo', 'hb'], percent_top=None, log1p=True, inplace=True)
# log1p는 로그 변환 log(1+x)임 1을 더하는건 count가 0인세포도 존재해서 log(0)은 -무한이라 1더해서 방지

print(adata.obs.columns.tolist())

# pl은 plotting - 시각화 담당
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True)
# 하나 더 있는데 tl은 tools - 분석 알고리즘(PCA, UMAP, clustering 등)
```

<aside>
💡

#### log1p에서 로그변환이 뭘까?

일단 log는 ‘이 수가 몇번 곱해져야 이 값이 되냐’ 임

```python
log₂(8) = 3   →  2를 3번 곱하면 8
log₂(1024) = 10  →  2를 10번 곱하면 1024
```

왜 scRNA-seq에서 log변환을 하냐고 묻는다면
count 데이터가 예를 들어 이렇게 생겼다고 가정해보자

```python
유전자A: 0, 0, 1, 2, 3, 5000
```

대부분이 0이고 일부가 5000까지 튄다고 가정 했을 때 해당 유전자 데이터는 저 5000이라는 데이터 하나가 분석을 모두 왜곡 시키게 됨

이때 로그를 변환하면

```python
0    → log(1+0) = 0
1    → log(1+1) = 0.69
100  → log(1+100) = 4.6
5000 → log(1+5000) = 8.5
```

극단적으로 올라가 있던 값이 줄어들어서 분포가 고루 퍼짐

- log1p에서 1인 이유는 count가 0인 세포가 많으니까 log0을 넣으면 무한대로 빨려들어가서임
- 1p는 1plus임 log에 ‘1 더한 다음 log’ 연산 하라는 뜻
</aside>

- 시각화 시킨 컬럼 들의 의미
    1. n_genes_by_counts
    : 세포 당 검출 된 유전자 수
        
        정상 세포는 수백~수천 개 유전자를 동시에 발현 함. 너무 적으면 세포막이 터져서 mRNA가 다 빠져나간 빈 droplet 이거나 죽은 세포인거고 너무 많으면 두 세포가 한 droplet에 잡힌 doublet임
        
        너무 적다의 기준은 한 200 이하 쯤(내 그래프에서), 상위 극단 값이 그래프에 찍혀 있다면 너무 많은 것
        
    2. total_counts 
    : 세포 당 UMI/count 합 → sequencing depth랑 관련 이 크다
        
        (sequencing depth란 유전자 염기서열 분석 시 특정 염기나 영역이 평균적으로 몇번이나 중복되어 읽혔는지를 나타내는 지표)
        
        유전자가 많이 발현될수록  count가 높다. 너무 낮으면 세포 상태가 나쁜거고 너무 높으면 doublet임
        
        정상 값은 데이터 분포의 중앙 값을 기준으로 하고 분포에서 극단적으로 벗어났을 경우엔 비정상으로 간주한다.
        
    3. pct_counts_mt 
    : 미토콘드리아 비율
        
        세포가 죽어가면 세포막이 터지면서 세포질 mRNA는 빠져나가고 미토콘드리아 mRNA만 남는다. 그래서 mt비율이 높을수록 죽어가는 세포
        
        정상치가 보통 5~20%인데 20~25% 이상이 넘어간다면 비정상을 의심해보아도 됨
        
    4. pct_counts_mt
    : 전체 count 중 미토콘드리아의 비율(%)

![image.png](attachment:519ce143-a0ce-43b5-855e-296332e930a3:image.png)

- 그래프 해석
    1. n_genes_by_counts
        
        : 대부분의 세포가 0-2000 값에서 형성 되어있으나 일부 값이 8000까지 튀어있는 것을 보아 위로 튄 값은 doublet 의심
        
    2. total_counts
        
        : 대부분 낮은 count값을 가지고 있는데 일부 세포가 40000까지 튀어있는 것을 보아 위로 튄 값은 비정상 의심
        
    3. pct_counts_mt
        
        : 정상이면 20% 이하여야 하는데 100까지 퍼져 있는 것을 보아 죽은 세포가 많은 것으로 보임
        

## 2. MAD 필터링 적용

### MAD란?

MAD: Median Absolute Deviation 데이터 분포에서 중앙값 기준으로 얼마나 벗어 났는지를 측정하는 것

고정 값(20% 이상 제거)을 사용하면 데이터마다 기준이 달라져서 문제가 생기는 반면에 MAD는 이 데이터의 분포 기준으로 자동을 잡아줘서 많이 사용 하는 편임

```python
import numpy as np
from scipy.stats import median_abs_deviation

# metric은 MAD 지표가 될 데이터가 들어갈 매개변수이고 nmads는 배수(몇배까지 허용할건지)
def is_outlier(adata, metric: str, nmads: int):
    M = adata.obs[metric]
    # outlier는 중앙값 ± (nmads × MAD) 범위를 벗어난 세포라는 것
    # True면 제거 대상, False면 정상.
    outlier = (M < np.median(M) - nmads * median_abs_deviation(M)) | \
              (np.median(M) + nmads * median_abs_deviation(M) < M)
    return outlier

adata.obs['outlier'] = (
    is_outlier(adata, 'log1p_total_counts', 5)
    | is_outlier(adata, 'log1p_n_genes_by_counts', 5)
)

adata.obs['mt_outlier'] = is_outlier(adata, 'pct_counts_mt', 3) | (adata.obs['pct_counts_mt'] > 20)

# log1p_total_counts와 log1p_n_genes_by_counts의 MAD 적용한 outlier 결과 출력
print(adata.obs['outlier'].value_counts())
# pct_counts_mt의 MAD 적용한 outlier 결과 출력
print(adata.obs['mt_outlier'].value_counts())
```

![image.png](attachment:3e9e38b0-0cf3-4329-9021-d5cf4af451c3:image.png)

### 결과값 분석

outlier:  173954개 모두 False. 즉 total counts랑 n genes 기준으로는 이상한 세포가 없다

mt_outlier:  57972개가 True. 전체의 약 33%가 제거 대상. → 아까 시각화 한 바이올린 플롯에서 mt가 100까지 튀었던 것 일듯

```python
print(f'필터링 전 세포 수: {adata.n_obs}')
adata = adata[(~adata.obs['outlier']) & (~adata.obs['mt_outlier'])].copy()
print(f'필터링 후 세포 수: {adata.n_obs}')

sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True)
```

![image.png](attachment:efef342e-c660-4597-8c0e-f452aa574167:image.png)

![image.png](attachment:9683a54e-2f15-4162-9ca8-6d0c607aaea2:image.png)

### QC적용 완료 된 그래프

- pct_counts_mt: 아까 100%까지 튀었었는데 이제 20% 이하로 깔끔하게 잘렸음
- n_genes_by_counts, total_counts: 분포는 거의 동일, outlier가 전체 False니까 당연한 결과

*26.05.03 - 커밋 완료*

---

# 2. Normalization 진행

## Normalization이란?

: 세포마다 sequencing depth가 다르다. 어떤 세포는 10000개 일 수도 있고 어떤 세포는 1000개가 잡힐 수도 있는데 이러면 단순 비교가 불가능하다. 

그러면 더 많이 읽힌 세포가 모든 유전자가 발현이 높아 보일 수 있으니까 세포 별 total count를 맞춰 주는 것임

유전자끼리 맞춰주는게 아니라 세포간 library size를 맞춰주는 것임

```python
# raw data 보존 - 나중에 DEG 분석 시 사용 할 것
adata.layers['counts'] = adata.X.copy()

# 1e4는 앞에는 1이고 지수에 10^4
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

print(adata)
```

![image.png](attachment:5566c24b-583f-4b61-9757-000a6bf248c6:image.png)

- 주목 해야 할 점이 있음
: 경고에 Some cells have zero counts 라고 찍혀있음
    
    QC 이후에도 total count가 0인 세포가 남아있다는 뜻임. 이런 세포는 normalization 할 때 0으로 나누기가 발생해서 문제가 될 수 있으니까 제거하고 가는 것이 좋음
    

```python
# normalize_total 실행 시 'Some cells have zero counts' 경고 발생
# QC 후에도 total count = 0인 세포가 남음 -> 0으로 나누기 방지를 위해 먼저 제거

sc.pp.filter_cells(adata, min_counts=1)
print(f'0 count 제거 후: {adata.n_obs}')

# raw count 보존
adata.layers['counts'] = adata.X.copy()

# normalization
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

print(adata)
```

결과 값

```markdown
0 count 제거 후: 115909
WARNING: adata.X seems to be already log-transformed.
AnnData object with n_obs × n_vars = 115909 × 41861
    obs: 'n_genes_by_counts', 'log1p_n_genes_by_counts', 'total_counts', 'log1p_total_counts', 'total_counts_mt', 'log1p_total_counts_mt', 'pct_counts_mt', 'total_counts_ribo', 'log1p_total_counts_ribo', 'pct_counts_ribo', 'total_counts_hb', 'log1p_total_counts_hb', 'pct_counts_hb', 'outlier', 'mt_outlier', 'n_counts'
    var: 'mt', 'ribo', 'hb', 'n_cells_by_counts', 'mean_counts', 'log1p_mean_counts', 'pct_dropout_by_counts', 'total_counts', 'log1p_total_counts'
    uns: 'log1p'
    layers: 'counts'
```

warning 뜨는 것은 QC 지표 계산할 때 이미 log1p=True로 전환했는데 또 찍어서 이미 log변환된거 아니냐고 경고 띄우는 것인데 아까 calculate_qc_matrics의 log1p는 qc지표 컬럼들만 변환한거라서 adata.x 자체는raw count 그대로 였어서 상관없음.

즉  normalization total의 logp1가 adata.x에 처음 적용 된거라 잘 한거임

<aside>
💡

#### target_sum=1e4 (10,000) 으로 설정한 이유:

bulk RNA-seq의 CPM(Counts Per Million)에서 착안한 방식이다.
단, scRNA-seq는 세포당 포착되는 mRNA 수가 bulk 대비 훨씬 적기 때문에
1,000,000 대신 10,000을 기준값으로 사용하는 것이 scRNA-seq 분야의 관례다.
Seurat, Scanpy 공식 튜토리얼 모두 동일한 값을 사용한다.

</aside>

<aside>
💡

#### 정규화 코드리뷰

```python
# normalization
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
```

#### normalize_total

세포마다 sequencing depth가 다름

예를들어

```python
Cell A total count = 50,000
Cell B total count = 5,000
```

라고 한다면 A가 그냥 더 많이 읽힌 것 뿐인데 모든 유전자 발현이 높아 보일 수 있음

⇒ 그래서 세포 별 total count를 맞춰주는 것임

유전자끼리 맞춰주는 것이 아니라 세포 간 library size를 맞춰주는 것

#### log1p

scRNA count 분포는 극단적으로 치우쳐져 있는 경우가 많음(skewed)

예를 들어 이런 식 → 0 0 0 1 2 5 1000

- variance 너무 큼
- PCA/HVG/dist 계산 불안정
- high-expression gene 지배

그래서 ***dynamic range*** 압축을 하려고 log를 사용

log(0)은 안되니까 log(1+x)를 사용해서 l임

</aside>

*26.05.04- 커밋 완료*

---

# 3. HVG 진행

HVG(High Variable Gene) - 41861개의 유전자 중에서 세포마다 발현량 차이가 큰 유전자만 골라 내는 것.

차이가 없는 유전자는 세포 타입 구분에 쓸모가 없으니까 제거하고 분석 효율을 높이는 방법이다

즉 클러스터 구분에 informatice한 유전자를 골라내는 방법임

⇒ 어떤 세포에서나 발현되는 유전자는 분별력이 떨어지고 특정 세포에서 다수로 혹은 소수로 나타나는(세포마다 발현량이 들쑥날쑥한 유전자) 유전자가 판단의 기준이 되기 때문에 유전자들 중에서 변별력/분별력이 있는 유전자들만 위에서부터 카운트하여 그 밑은 잘라낸다는 뜻이다

예를들어

- CD3D: T세포에서만 높게 발현, 나머지 세포에서는 거의 0 → 분별력 높음 → HVG 선택
- housekeeping gene(GAPDH 같은 것): 모든 세포에서 비슷하게 발현 → 분별력 없음 → 제거

```python
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor='seurat_v3', layer='counts')

print(f'HVG 수: {adata.var.highly_variable.sum()}')
sc.pl.highly_variable_genes(adata)
```

![image.png](attachment:cfefc238-d859-4d69-bbed-8701ec236b58:image.png)

#### 그래프 해석

- 검은 점 = HVG 2000개 - 세포마다 발현 차이가 큰 유전자
- 회색 점 = 나머지 39861개 - 차이가 별로 없어서 제외

→ 왼쪽 그래프(normalized)에서 분산 높은 유전자 군이 상단에 명확하게 분리되어 있어 2,000개 선택이 이 데이터에서도 유효함을 시각적으로 확인할 수 있다

<aside>
💡

#### 세포마다 발현 차이가 큰 유전자가 무엇을 의미할까?

예를 들어서

유전자 A: 모든 세포에서 발현량이 100, 100, 100, 100 → 차이없음
*= 세포 타입 구분에 쓸모가 없다*
유전자 B: 세포마다 발현량이 0, 0, 500, 300 → 차이가 큼
*= 이 유전자가 많이 발현되는 세포는 특별한 타입이구나 구분 가능*

즉 세포 타입을 구별하는 데 유용한 유전자를 골라내는 것

모든 세포에서 똑같이 발현되는 유전자는 구분에 도움이 안되니까 제외하는 것

</aside>

<aside>
💡

#### 왜 n_top_genes=2000 로 두었는가?

HVG 그래프에서 검은 점(HVG)과 회색 점(non-HVG)이 명확히 분리되어 있어 2000개 선택이 이 데이터에서 유효함을 시각적으로 확인했다.

개수(2000개)는 Seurat/Scanpy 공식 기본값이며,
너무 적으면(500개 이하) 세포 타입 구분에 필요한 유전자가 빠질 수 있고
너무 많으면(10,000개 이상) 노이즈 유전자까지 포함되어 분석이 왜곡된다.

이 trade-off에서 경험적으로 검증된 값이 2000~3000개이며, 본 데이터에서도 그래프 상 분리가 명확하므로 2000개를 채택했다.

</aside>

<aside>
💡

#### 발현량이 높은 유전자와 변동이 큰 유전자는 같은 뜻일까?

***⇒ 비슷하지만 다르다***

발현량이 높은 유전자는 말그대로 특정 세포에서 발현이 많이 된 유전자를 나타내는 것

변동성이 큰 유전자는 어떤 세포에서는 엄청 많은데 어떤 세포에서는 엄청 적거나 없다 이럴때 쓰는 말이니까 의미가 약간 다름

</aside>

<aside>
💡

#### normalization 전에 HVG를 하면 안될까?

***⇒ 안된다.***

유전자 발현량을 미리 맞춰주고 나서 유의미한 유전자를 잘라줘야 하는건데 먼저 자르기부터 시작하면 어떤건 많고 어떤건 적고 노이즈가 생길 수 밖에 없고 동일한 조건에서 비교가 불가능하기에 유의미하다 또는 아니다 판단 자체가 왜곡 될수 밖에 없음

더욱 정확하게 말하자면 normalization을 하지 않으면 seqencing depth 차이가 variance처럼 보일 수 있음
**많이 읽힌 cell → 모든 gene variance 커 보임(정규화 하는 이유)**

⇒ 그래서 fake HVG가 생길 수 있다는 뜻임

결론: 순서를 지키자

</aside>

![image.png](attachment:b884f858-15c4-4b3c-a238-1507de637e8d:image.png)

위에 shape로 출력 된 값을 보면 115909개의 세포와 2000개의 유전자로 HVG를 통해 줄어든 것을 확인 가능

# 4. PCA 진행

2000개의 유전자 정보를 더 적은 차원으로 압축하는 작업

2000개의 차원 데이터를 그대로 사용하면 계산이 너무 오래 걸리고 노이즈도 많기 때문에 비슷한 정보끼리 묶어서 압축 하는 작업

차원 = 데이터를 설명하는 변수의 수
세포 한 개에 컬럼 수가 41861개 들어있는 상태 → 시각화가 불가능
2차원 그래프는 x좌표와 y좌표만 있으면 되기 때문에 시각화가 가능한거고
4+n차원들은 더이상 평면으로 표시가 불가능하기 때문에 수학적 이론으로만 존재

→ PCA는 2000차원을 50차원으로 압축하는 작업이고 최종적으로 UMAP이 그걸2차원으로 펼쳐서 시각화한다. PCA단계에서 몇개의 차원(PC)까지 쓸지는 variance ratio 그래프의 elbow 지점을 보고 결정한다

여기서 한가지 중요한 점이 있음

PCA는 새로운 축을 생성하는 것임 → 이 개념이 중요함

```python
CD3D ↑
IL7R ↑
LTB ↑
```

이 세 유전자가 T cell에서 같이 움직이면
PCA는 ‘얘네를 하나의 방향으로 표현 가능하네’ 라고 볼 수 있는 것임

즉, gene space를 → latent feature space로 보는 것

elbow = 그래프에서 꺾이는 지점

```python
분산
│\
│  \
│    \
│      \_______________  ← 여기가 elbow
│
└─────────────────── PC 번호
  1  2  3  4  5 ... 17 18 19 ...
```

- PC1~4: 가파르게 떨어짐 → 정보가 많다
- PC17 이후: 완만해짐 → 추가 정보가 거의 없다
- **elbow = 완만해지기 시작하는 PC17 지점**

threshold랑 비슷한데 차이는:

- threshold는 **미리 정해놓은 기준값** (예: 20% 이상 제거)
- elbow는 **데이터 그래프를 보고 판단하는 지점** → 데이터마다 다르다

```python
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver='arpack')
sc.pl.pca_variance_ratio(adata, log=True)
```

![image.png](attachment:ed00d078-2cab-4816-a8bb-906ef8c4dd91:image.png)

#### 그래프 해석

PCA는 2000개 유전자 정보를 PC1, PC2, PC3 …순서로 압축한다
PC1이 가장 많은 정보를 담고 뒤로 갈 수록 담는 정보가 줄어든다

x축 = PC 번호 순서
y축 = 각 PC가 담고 있는 분산 비율(log scale)

- PC1~PC4 구간이 가파르게 떨어짐 → 이 PC들이 데이터 정보를 많이 담고 있다
- PC10 이후부터 완만해짐 → 추가 정보가 별로 없다

<aside>
💡

#### PCA를 왜 하나요?

UMAP이랑 clustering을 진행 할 때 PC를 몇개 사용할지 결정하기 위해서 미리 지표로 그려보는 것이다

그래프가 완만해지는 시점까지 쓰면 되는데 내가 보고 있는 데이터 기준으로는 PC 15~20 정도까지 쓰면 될 듯 싶다

→ 그렇게 판단한 이유는 그 이후로는 오히려 데이터의 노이즈가 될 것 같음 (추가 정보가 없는 번호들이니까)

</aside>

<aside>
💡

#### svd_solver=’arpack’와 다른 옵션들

SVD는 PCA를 계산하는 수학적 방법이다

PCA를 계산할 때 내부적으로 행렬 분해를 해야하는데 그 방법이 여러가지이다
svd_solver는 그 방법을 선택하는 옵션

arpack은 그 중 하나로 대용량 sparse 행렬에 최적화 된 방법이다
내가 선택한 데이터가 115909x2000짜리 행렬이니 arpack을 선택한 것

- **다른 옵션들**
    - auto    → 데이터 크기 보고 자동 선택
    - full    → 소규모 데이터용 (전체 계산)
    - arpack  → 대용량 sparse 데이터용
    - randomized → 근사값으로 빠르게 계산
</aside>

<aside>
💡

#### PC의 의미가 뭘까

***⇒ PC = variance 방향***

이때 PC는 principal component임

PC1 = 데이터에서 가장 큰 variation
PC2 = 그 다음 variation

라고 예시를 들 때 

- cell type 차이
- activation state
- cell cycle
- batch

같은 것들이 variance 축이 됨

**즉, 세포들을 가장 잘 구분하는 방향 이라고 생각 하면 된다**

</aside>

<aside>
💡

#### 왜 neighbors graph를 raw gene matrix 가 아니라 PCA 결과 공간에서 만들까?

raw gene matrix가 20000genes라고 친다면 이건 너무 고차원에 + noisy함

그래서 거리 계산하면 noise 영향이 엄청 큼

PCA는 biological signal 남기고 noise 줄인 latent space를 만드니까 neighbors는 PCA reduced space에서 계산하는 것임

즉 ***정제 된 feature space에서 세포 유사도를 계산***하는 느낌이라고 보면 됨

</aside>

# 4. UMAP 진행

PCA로 줄인 차원을 사람의 눈으로 볼 수 있도록 2차원으로 펼치는 작업

- embedding
    
    PCA를 돌리면 각 세포가 50차원 공간의 점으로 표현 됨. 이것을 임베딩이라고 함
    
    → 고차원 데이터를 숫자 좌표로 바꾼 것
    

비슷한 유전자 발현 패턴을 가진 세포끼리 가까이 배치된다

```python
sc.pp.neighbors(adata, n_pcs=15)
sc.tl.umap(adata)
sc.pl.umap(adata)
```

![image.png](attachment:c74ea275-05b1-4bac-a840-44bb9577e4e1:image.png)

<aside>
💡

#### n_neighbors=15 값이 너무 작거나 크면 어떻게 될까?

n_neighbors값이 너무 작으면 너무 조각조각 나눠져서 overclustering되고

너무 크게 묶으면 특성이 섞여 버릴 것임 -> 데이터 왜곡

</aside>

<aside>
💡

#### 가까우면 biology 적으로 반드시 가까운가?

***⇒ 아님***

가까운 세포끼리 군집을 시키는 함수라고 해서 가까우면 무조건 생물학적으로 비슷한가 라고 묻는다면 답은 아니다 이다

UMAP은 local neighborhood preservation 중심

즉 가까운게 어느정도 의미가 있는건 맞는데 ***멀다고 biology적으로 멀다는 보장은 없음***

왜냐면

- 2D projection
- manifold approximation
- global distance 왜곡

같은 것이 생기기도 함

</aside>

# 5. Clustering 진행

비슷한 세포끼리 같은 그룹으로 묶는 계산을 수행한다
UMAP가 단순 시각화라면 Clustering은 실제로 이 세포들은 0그룹, 저 세포들은 1그룹 하고 번호를 붙이는 작업이라고 구분 하면 된다 (라벨링)
위 UMAP 표에서 회색으로만 표시 되는 그래프를 각각 클러스터 번호에 따라 색을 입혀서 가독성을 높여줄 수 있다

```python
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color='leiden')
```

- **resolution=0.5**
    
    → 클러스터를 얼마나 잘게 나눌지 조절하는 값
    
    resolution 낮음 (0.1~0.3) → 클러스터 적게, 크게 묶음
    resolution 중간 (0.5)     → 표준
    resolution 높음 (1.0~2.0) → 클러스터 많이, 잘게 쪼갬
    
    0.5는 관례적인 시작 값이고 나중에 annotation 하면서 클러스터가 너무 뭉쳐있어 보인다면 올리고 너무 잘게 쪼개져 있으면 내리는 식으로 조절 하면 되는 것
    

![image.png](attachment:530e69a3-f95f-4efa-b55c-4aa386fae3cf:image.png)

- 클러스터가 너무 잘게 쪼개져서 색이 다 비슷해 보이는 것으로 추정

```python
sc.tl.leiden(adata, resolution=0.005) # 0.5 -> 0.005로 낮춰서 다시 진행
sc.pl.umap(adata, color='leiden')
```

![image.png](attachment:d29af139-39b8-4f76-85b3-a4131dcbfc39:image.png)

- 뭔가 이상한 것 같다 resolution을 아무리 낮춰도 130개 이상이라는 것은 데이터 문제라고 판단

![image.png](attachment:7eb9320d-f2d4-4ca8-9669-c79aef31f3fe:image.png)

- 클러스터 0번에 108574개가 물려있고 나머지는 아주 소수만 들어있음
    
    ⇒ 완전한 불균형 상태
    
- 이것은 resolution 문제가 아니라 **batch effect** 문제이다
처음에 raw data sample을 26개를 합쳤으니 샘플마다 기술적 차이가 클러스터링을 왜곡 하는 듯함
- 이럴 때에는 **Harmony**로 **batch correction**을 해줘야 한다

<aside>
💡

#### 용어 정리

1. **batch effect**
    
    같은 실험을 해도 날짜, 실험자, 기기가 다르면 **기술적 차이가 발생**
    26개의 샘플이 각각 다른 환자, 다른 시점에 체취된 거라 샘플마다 기술적 노이즈가 다름
    그래서 클러스터링 할때 **생물학적으로 비슷한 세포끼리 묶이는 것**이 아니라 **같은 샘플끼리 묶이는 문제**가 발생 하는 것
    
    판단 기준은 클러스터 0에 108574개가 물리고 나머지가 다 작은건 비정상적임
    정상이라면 여러 클러스터에 고르게 분포해야 함
    
    ⇒ **이런 패턴이 batch effect의 전형적인 증상**
    
2. **batch correction**
    
    샘플마다 다른 기술적 노이즈를 제거해서 생물학적 신호만 남기는 작업
    
3. **Harmony**
    
    batch correction 툴 중 하나이다
    
    PCA 결과를 샘플 별로 보정해주어서 샘플 출처에 상관없이 비슷한 세포끼리 모이게 만든다
    
    이때 샘플 정보 컬럼이 필요한 이유는 Harmony한테 이 세포는 0번 이 세포는 1번 이런식으로 알려줘야 샘플 별로 보정이 가능하다
    ⇒ 이것이 sample 컬럼
    
</aside>

### batch correction 작업

1. 샘플 정보가 obs에 들어있는지 확인
    
    ```python
    print(adata.obs.columns.tolist())
    ```
    
2. 없는 경우 샘플 번호를 추출
    
    ```python
    adata.obs['sample'] = adata.obs_names.str.split('-').str[-1]
    print(adata.obs['sample'].value_counts())
    ```
    
3. Harmony로 batch correction 진행
    
    ```python
    # ~~pip insatall harmonypy 설치하고 진행~~
    # conda install -c bioconda harmonypy 설치하고 진행
    
    import scanpy.external as sce
    
    sc.pp.pca(adata, svd_solver='arpack')
    sce.pp.harmony_integrate(adata, 'sample')
    sc.pp.neighbors(adata, use_rep='X_pca_harmony')
    sc.tl.umap(adata)
    sc.tl.leiden(adata, resolution=0.5)
    sc.pl.umap(adata, color='leiden')
    ```
    
    Harmoney가 하는 일
    : 같은 세포 타입끼리는 샘플 상관없이 좌표를 비슷하게 맞춰 주는 것
    이렇게 조정 된 좌표가 X_pca_harmony
    
    ⇒ 그러면 이 보정된 좌표를 가지고 UMAP이 2D로 펼치는 것
    
4. 트러블 슈팅
    
    conda prompt에 라이브러리 설치 하다가 에러가 발생
    
    ![image.png](attachment:b134e514-926d-4edc-a1c8-621c3c7d1370:image.png)
    
    이런 오류 나오면 cMake에러 즉 빌드 도구 문제임
    
    conda install -c bioconda harmonypy 로 진행
    

```python
ValueError: Value passed for key 'X_pca_harmony' is of incorrect shape. Values of obsm must match dimensions ('obs',) of parent. Value had shape (50,) while it should have had (115909,).
```

에러 보면 키 값이랑 value shape 문제 발생했다고 뜸

아까 먼저 진행한 pca 기반으로 harmony를 돌린 것이 문제 인듯함

pca하고 나서 클러스터에서 문제가 발생한 것을 알았고 그때 sample 컬럼을 obs에 추가하면서 이전 데이터 값 기준으로 생성 된 키 값이 문제가 된듯함

즉 adata.obsm[’X_pca’]가 이전 HVG 필터링 기준으로 만들어진 것이라 shape가 안맞은 것

현재 데이터 기준으로 pca 다시 돌려서 진행하면 에러가 픽스 될 것으로 예상

```python
sc.pp.pca(adata, svd_solver='arpack')
print(adata.obsm['X_pca'].shape)  # (115909, 50) 이어야 함
```

shape 값을 제대로 할당해주었는데도 동일한 에러가 발생 → harmony 버전 문제라고 추측

```python
import harmonypy as hm
import pandas as pd

pca_result = adata.obsm['X_pca']
meta = adata.obs[['sample']]

ho = hm.run_harmony(pca_result, meta, 'sample')
adata.obsm['X_pca_harmony'] = ho.Z_corr

sc.pp.neighbors(adata, use_rep='X_pca_harmony')
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color='leiden')
```

코드 수정해서 umap 다시 시각화 해보았다

![image.png](attachment:58994580-9e81-464b-93cd-f4588fa5c6e9:image.png)

umap 모양은 훨 나아졌지만 여전히 클러스터가 너무 많아서 resolution값을 0.1로 낮춤

여러 번 시도 한 결과 여전히 클러스터는 너무 많이 생성이 됨

![image.png](attachment:fd8cc8e5-cdf7-4075-86fd-126b5af7a7ff:image.png)

harmony는 제대로 적용이 되어서 데이터 불균형은 좀 잡힌 것을 확인

그 뜻은 데이터 자체가 노이즈가 덜 걸러졌다는 것 같아서 n_pcs=10으로 umap를 진행해서 시각화 해보고 다시 클러스터링을 진행 해볼 생각

#### 두가지 방향이 있음

1. sc.pp.neighbors(adata, *n_pcs*=10) 로 진행했을 때 효과적으로 클러스터가 줄어든다면 그대로 진행
2. sc.pp.neighbors(adata, *n_pcs*=10) 으로 진행을 했는데도 클러스터가 필요 이상으로 많다면 데이터 자체가 복잡한 데이터인 것이라 (실제로 세포 115909개에 샘플 26개)다시 pcs=15로 롤백하고 annoation할때 주요 세포 타입만 골라낼 생각

*26.05.06- 커밋 완료*

---

### 1. n_pcs = 10으로 진행해보기

umap를 시각화하는 단계에서 sc.pp.neighbors(adata, *n_pcs*=10)로 수정을 하여 세포 간 거리를 계산 할 때 PC를 10까지만 사용해보자

나머지 로직은 그대로 진행한다.

돌리기 전에 매번 새로 실행하면 26개 파일 로딩+QC+nomalization을 해야 하니까 현 상태에서 저장을 한번 해주자

```python
adata.write_h5ad('dataset/GSE127465_human_qc_norm.h5ad')
print('저장 완료')
```

![image.png](attachment:110cf68e-daff-4c31-85f2-856bf104d4e7:image.png)

- 오히려 클러스터가 harmony를 적용했음에도 불구하고 클러스터 0에 111377개의 데이터가 몰려있음

![image.png](attachment:77a5dedd-bd56-43e0-92d4-880cb0a06bb2:image.png)

- obsm키 값에 harmony가 적용되어 있는지 확인
    
    → 되어있음
    

![image.png](attachment:c535034b-6fb3-4d26-8822-45c5f5e10bef:image.png)

- neighbors 돌릴 때 harmony가 적용이 안되었나 확인
    
    → 적용이 잘 되어있음
    

⇒ use_rep도 맞고 shape도 맞는데 클러스터에 0이 몰린다면 harmony가 수렴은 했는데 보정이 충분하지 않다는 것

![image.png](attachment:312e1e67-ddba-4340-96db-cc5aca38da6f:image.png)

- 샘플 별로 색을 입혀서 보면 샘플이 제대로 섞여있는지 확인 이 가능
    
    → 그래프를 보니 잘 섞여있긴 함
    

```python
sc.pp.neighbors(adata, use_rep='X_pca_harmony', n_pcs=10)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.03)
print(adata.obs['leiden'].nunique())
sc.pl.umap(adata, color='leiden')
```

![image.png](attachment:a90d1a96-6f2f-4fea-ad6b-9ec6f8bd6da0:image.png)

#### 결론

n_pcs를 10으로 조정해도 마찬가지로 클러스터링이 제대로 되지 않는다

데이터 자체가 워낙 복잡하고 많기 때문에 수렴이 잘 되지 않는 듯함

어쩔 수 없이 2번 선택지인 annotation 단계에서 주요 세포 타입만 골라내는 방식으로 가야 할 것 같음

### 2. n_pcs=15로 롤백 후  annotaion 단계에서 주요 세포 타입 골라내기

```python
sc.pp.neighbors(adata, use_rep='X_pca_harmony', n_pcs=15)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.3)
print(adata.obs['leiden'].nunique())
sc.pl.umap(adata, color='leiden')
```

![image.png](attachment:ceedbeee-0c0e-4d08-be0b-7b42e6a1e88e:image.png)

→ 총 클러스터 수: 127개

```python
adata.write_h5ad('dataset/GSE127465_human_clustered.h5ad')
print('저장 완료')
```

클러스터까지 진행한 파일 저장하고 다음 단계 annotation에서 주요 세포 타입 골라내기 진행

<aside>
💡

#### UMAP 시각화 그래프 모양이 같은 데이터로 돌리는데 왜 매번 다른가?

UMAP이 random initialization이라서 돌릴 때마다 모양이 달라질 수 있다

무슨 뜻이냐면 UMAP이 초기값을 랜덤으로 잡고 시작하는데 그것이 매번 달라서 모양이 달라지는 것.

만약 고정하고 싶다면 random_state를 설정해주면 된다

```python
sc.tl.umap(adata, random_state=42)
```

</aside>

<aside>
💡

#### AnnData 반복 실행 문제 없나?

대답은 “***반복 실행은 문제가 되지 않는다.”
파라미터 튜닝 시, 덮어씌워지는 영역이 다르기 때문이다.***

neighbors, umap, leiden을 같은 adata에 반복해서 돌려도 데이터가 꼬이지 않는다.

- **adata.X, adata.obs, adata.var** → 원본 데이터, 변하지 않음
- **adata.obsm** → UMAP, PCA 결과 저장 (덮어쓰기)
- **adata.obsp** → neighbors 그래프 저장 (덮어쓰기)
- **adata.uns** → 파라미터 정보 저장 (덮어쓰기)
</aside>

<aside>
💡

#### Leiden graph clustering

neighbors 단계에서 세포 관계망(graph)을 이미 만든 것임

Leigen은 연결이 강한 community를 찾자! 하는 알고리즘임

즉 단순 거리보다는 network structure를 찾는 것

</aside>

<aside>
💡

#### resolution 의미

***⇒ cluster granularity 조절***

resolution값이 낮으면 큰 cluster 몇개만 나오고 높으면 잘게 쪼개짐

즉, 얼마나 잘게 나눌지를 조절하는 것임

</aside>

<aside>
💡

#### overclustering의 원인들

- noisy cell
- QC 부족
- 찌꺼기 cluster
- 의미 없는 subcluster
- resolution 너무 높음
- n_neighbors 너무 작음
- batch correction 실패
- doublet
- low-quality cell
- PCA 차원 너무 많음

노랑표시는 내 데이터의 경우였다

</aside>

*26.05.07- 커밋 완료*

---

# **[Troubleshooting: The MAD Trap]**

### 회고

Phase 1 문서 검토 중 클러스터 과다 생성의 근본 원인을 파악함

문서 검토 결과 n_genes_by_counts와 total_counts가 너무 낮아도 이상치라는 것을 적용하지 않음을 깨닳음 그리고 MAD 필터를 단독으로 적용하여 n_genes_by_counts와 total_counts의 outlier가 False로 출력되어 데이터 필터링이 아예 안 들어감

<aside>
💡

#### 왜 MAD 가 False 로 출력했는가?

그래프를 다시 확인해보니 명확하게 보인다

low count 세포가 너무 많음
→ 중간 값(median) 자체가 낮게 형성됨
→ low count 세포도 ‘중간 값 근처’로 인식
→ outlier 아님으로 판정

</aside>

low count 세포가 데이터 내 다수를 차지할 경우 MAD의 중앙값 자체가 낮게 형성되어 low count 세포도 정상으로 판정되는 문제가 있었던 것

이 상태로 정규화 및 클러스터링을 진행했기 때문에 노이즈 세포가 독립 클러스터로 분류되어 총 클러스터 수 127개라는 비정상적인 클러스터 수가 발생한 것으로 판단

### 재진행 계획

1-2 QC 재진행

- MAD 필터 + 하드 컷오프 병행 적용
    - n_genes_by_counts < 200 제거
    - total_counts < 500 제거
- Doublet 제거 (scDblFinder 또는 Scrublet)

2-2 정규화 재진행

3-2 HVG → PCA → Harmony → UMAP → 클러스터링 재진행 후 최종적으로 노이즈가 빠진 클러스터링 그래프 시각화

*26.05.08- 커밋 완료*

---

# 1-2 QC 재진행

![image.png](attachment:3d674e85-7c6a-4d5b-ac3a-65ad4c76ea72:image.png)

이전 QC진행 후 그래프를 보면 n_genes_by_counts랑 total_counts가 0 근처에서 점이 엄청 깔려있다

저게 다 low count 세포들인데 평균 값 자체가 너무 낮다보니 MAD 중앙값이 낮게 잡혀서 outlier로 잡히지 않은 것

```python
import scanpy as sc
import numpy as np
from scipy.stats import median_abs_deviation

# MAD 필터 + 하드 컷오프 병행
adata = sc.read_h5ad('dataset/raw/GSE127465_human_all.h5ad')  # raw부터 다시

# QC 지표 계산
adata.var['mt'] = adata.var_names.str.startswith('MT-')
adata.var['ribo'] = adata.var_names.str.startswith(('RPS', 'RPL'))
adata.var['hb'] = adata.var_names.str.contains(r'^HB[ABDEGMQZ]\d*(?!\w)')
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt', 'ribo', 'hb'], percent_top=None, log1p=True, inplace=True)

# 하드 컷오프 기준 판단
print(adata.obs['n_genes_by_counts'].describe())
print(adata.obs['total_counts'].describe())

# 하드 컷오프
adata = adata[adata.obs['n_genes_by_counts'] >= 200].copy()
adata = adata[adata.obs['total_counts'] >= 500].copy()

print(f'하드 컷오프 후: {adata.n_obs}')

def is_outlier(adata, metric: str, nmads: int):
    M = adata.obs[metric]
    outlier = (M < np.median(M) - nmads * median_abs_deviation(M)) | \
              (np.median(M) + nmads * median_abs_deviation(M) < M)
    return outlier

# MAD 필터
adata.obs['outlier'] = (
    is_outlier(adata, 'log1p_total_counts', 5)
    | is_outlier(adata, 'log1p_n_genes_by_counts', 5)
)
adata.obs['mt_outlier'] = is_outlier(adata, 'pct_counts_mt', 3) | (adata.obs['pct_counts_mt'] > 20)

print(adata.obs['outlier'].value_counts())
print(adata.obs['mt_outlier'].value_counts())

# 필터링 적용
print(f'필터링 전: {adata.n_obs}')
adata = adata[(~adata.obs['outlier']) & (~adata.obs['mt_outlier'])].copy()
print(f'필터링 후: {adata.n_obs}')

# 시각화
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True)
```

![image.png](attachment:1ac4c5be-dc62-4712-8625-98002954be92:image.png)

![image.png](attachment:b8183994-4dea-4543-9297-94914810cefa:image.png)

- 이전에는 outlier가 전부 false였던 것에 비하여 이번엔 True가 135개로 잘 잡힘
→ 하드 컷 오프의 효과가 즉각적으로 나타남
    
    중앙 값이 올라가니까 mad도 제대로 작동한 것
    → 그래서 로직에서 하드 컷오프를 MAD보다 먼저 적용 하는 것이 중요함
    
- n_genes_by_counts와 total_counts의 위로 뻗은건 135개가 이미 잡혔음
- 하지만 doublet일 수 있으니까 로그를 찍어보았다

![image.png](attachment:29c90ffc-7340-4e69-8488-e0e0cdaf4d7b:image.png)

- 그래프에서 남아있는 것은 실제 생물학적으로 유전자가 많이 발현하는 세포 인듯함
- 분포가 적절히 섞여있고 무엇보다 아까 위로 뻗은 값이 MAD필터가 적용 된 것이기 때문에 QC는 여기까지만 진행하기로 결정

```markdown
### QC 그래프 확인 (Hard-cutoff & MAD 필터 적용 전)

**그래프 해석**
1. n_genes_by_counts
    
    : 대부분의 세포가 0-2000 값에서 형성 되어있으나 일부 값이 8000까지 튀어있는 것을 보아 위로 튄 값은 doublet 의심
    
2. total_counts
    
    : 대부분 낮은 count값을 가지고 있는데 일부 세포가 40000까지 튀어있는 것을 보아 위로 튄 값은 비정상 의심
    
3. pct_counts_mt
    
    : 정상이면 20% 이하여야 하는데 100까지 퍼져 있는 것을 보아 죽은 세포가 많은 것으로 보임

**Hard cutoff 기준 근거**
하드 컷오프 적용 전 전체 데이터 분포:
| 지표 | 25th percentile | 50th percentile | mean |
|------|----------------|----------------|------|
| n_genes_by_counts | 22 | 71 | 308 |
| total_counts | 41 | 125 | 711 |

25th percentile이 각각 22, 41에 불과할 정도로 low-count 세포가 다수를 차지하고 있었다.
이 상태에서 MAD를 적용하면 중앙값(71, 125)이 낮게 형성되어 low-count 세포도 정상으로 판정된다.

`n_genes_by_counts ≥ 200`: 정상 세포는 최소 수백 개 유전자를 동시에 발현한다.
200 미만은 세포막이 파괴되어 mRNA가 유출된 사멸 세포로 판단한다.
Seurat, Scanpy 공식 튜토리얼에서도 200을 하한선으로 사용한다.

`total_counts ≥ 500`: 신뢰할 수 있는 유전자 발현 정보를 얻으려면 최소한의 sequencing depth가 필요하다.
중앙값이 125에 불과한 상황에서 500은 노이즈 세포를 걸러내는 보수적인 기준이다.
```

# 2-2 정규화 재진행

마찬가지로 normalize_total 이 세포 당 총 count로 나누는데 total count가 0이면 0으로 나누기가 발생해서 에러가 생기니 먼저 제거하고 정규화 진행

```python
# 0 count 세포 제거
sc.pp.filter_cells(adata, min_counts=1)
print(f'0 count 제거 후: {adata.n_obs}')

# raw count 보존
adata.layers['counts'] = adata.X.copy()

# normalization
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

print(adata)
```

```markdown
# 결과 로그
0 count 제거 후: 44860
AnnData object with n_obs × n_vars = 44860 × 41861
    obs: 'n_genes_by_counts', 'log1p_n_genes_by_counts', 'total_counts', 'log1p_total_counts', 'total_counts_mt', 'log1p_total_counts_mt', 'pct_counts_mt', 'total_counts_ribo', 'log1p_total_counts_ribo', 'pct_counts_ribo', 'total_counts_hb', 'log1p_total_counts_hb', 'pct_counts_hb', 'outlier', 'mt_outlier', 'n_counts'
    var: 'mt', 'ribo', 'hb', 'n_cells_by_counts', 'mean_counts', 'log1p_mean_counts', 'pct_dropout_by_counts', 'total_counts', 'log1p_total_counts'
    uns: 'log1p'
    layers: 'counts'
```

- 0 카운트를 제거해도 값이  그대로 인 이유는 QC단계에서 total count ≥500을 걸어서(Hard-cutoff) 0 count 세포가 없기 때문이다 ← 그래도 방어 로직으로써 추가함

# 3-2 HVG → PCA → Harmony → UMAP → 클러스터링 순차적으로 재진행

```python
# HVG
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor='seurat_v3', layer='counts')

# annotation 시 HVG 외 marker gene 조회를 위해 전체 유전자 백업
adata.raw = adata

adata = adata[:, adata.var.highly_variable].copy()

# PCA
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver='arpack')
sc.pl.pca_variance_ratio(adata, log=True)
```

<aside>
💡

#### adata.raw=data backup 이유

adata = adata[:, adata.var.highly_variable].copy() 로 HVG를 적용하면 이후 adata 데이터 셋에는 non-HVG gene이 제거가 됨

근데 annotation이나 marker visualization은 꼭 HVG 이후 데이터만 보지 않음

그래서 raw data를 미리리 bak해두어야 함

</aside>

![image.png](attachment:81c622b8-51e7-4e23-9a60-7936716d2dcf:image.png)

- PC 1~4가 가파르고 PC17 이후부터 완만해지는 것이 보이니까 17까지 자를 것

```python
# sample 컬럼 추가
adata.obs['sample'] = adata.obs_names.str.split('-').str[-1]

# Harmony
import harmonypy as hm
pca_result = adata.obsm['X_pca']
meta = adata.obs[['sample']]
ho = hm.run_harmony(pca_result, meta, 'sample')
Z_corr = ho.Z_corr
if Z_corr.shape[0] != adata.n_obs and Z_corr.shape[1] == adata.n_obs:
Z_corr = Z_corr.T
assert Z_corr.shape[0] == adata.n_obs, f"Unexpected Harmony shape: {Z_corr.shape}"
adata.obsm['X_pca_harmony'] = Z_corr  # (n_cells, n_pcs)

# UMAP + clustering
sc.pp.neighbors(adata, use_rep='X_pca_harmony', n_pcs=17)
sc.tl.umap(adata, random_state=42)
sc.tl.leiden(adata, resolution=0.5)
print(adata.obs['leiden'].nunique())
sc.pl.umap(adata, color='leiden')
```

![image.png](attachment:f77e6666-6c2f-410b-a52f-40dc9fb09e3f:image.png)

- 이전과 비교했을 때 127개의 클러스터에 뭉쳐서 모두 회색이었던 것에 비해 이번 클러스터링은 성공적으로 진행된 걸 확인할 수 있다
- 15개의 클러스터와 군집이 명확하게 분리되어 색이 입혀져있다

*26.05.09- 커밋 완료*

---

# 6. Annotation 진행

어노테이션을 진행하기 전에 앞서
`sc.pl.umap(adata, color=['CD3D', 'CD68', 'EPCAM', 'CD19'], ncols=2)`
를 돌려서 markergene발현량을 확인

이때 CD3D 데이터가 유전자와 세포 데이터 컬럼에 존재하지 않는다는 것을 깨닳았음

![image.png](attachment:ebd03b89-6976-46fc-a834-93c0b5ae85c3:image.png)

HVG 필터를 적용하여 정규화 시 2000개로 데이터를 자르기 전에 RAW DATA를 미리 백업 해두었어야했는데 하지않고 바로 잘라버려서 marker gene 발현량을 확인 할 수가 없음

- adata에 백업하는 이유
    
    annotation을 할때 HVG에 없는 marker gene도 확인해야 하는데 sc.pl.umap(color=’CD3D’) 같은 함수가 자동으로 adata.raw에서 유전자를 찾아 오기 때문
    
    ![image.png](attachment:568b47c7-e4fb-4c69-977b-bb1034b1da96:image.png)
    

그래서 이번엔 hvg 로직 도중 필터 적용 직전에 직전 adata를 adata.raw에 백업 후 클러스터링까지 진행 (이전 로직 수정하여 추가하였음)

raw data 백업 후 `sc.pl.umap(adata, color=['CD3D', 'CD68', 'EPCAM', 'CD19'], ncols=2)` 를 진행하면 제대로 유전자 별 발현량이 나오는 것을 확인 할 수 있다

![image.png](attachment:6d91e120-4d18-4dfb-83db-73a68b351f96:image.png)

- 색이 진할수록 발현량이 높은 것

#### 그래프 해석

- **CD3D** → 왼쪽 중간 군집에서 발현 높음 → T세포 클러스터
- **CD68** → 오른쪽 군집에서 발현 높음 → 대식세포 클러스터
- **EPCAM** → 오른쪽 아래 군집에서 발현 높음 → 암세포 클러스터
- **CD19** → 위쪽 군집에서 발현 높음 → B세포 클러스터

```python
# 각 유전자 발현량을 그래프로 시각화
sc.pl.umap(adata, color=['CD3D', 'CD68', 'EPCAM', 'CD19'], ncols=2)
# leiden 클러스터 번호를 색을 입혀 시각화
sc.pl.umap(adata, color='leiden')
```

- 이 두개의 그래프를 나란히 두고 보면 몇번 클러스터가 어떤 세포의 군집인지 알 수 있다

![image.png](attachment:8d06bf7a-c949-42fa-a2c3-4ead749ac998:image.png)

![image.png](attachment:077e3ce7-594d-4bf7-9255-0dbd91f14e47:image.png)

#### 그래프 비교 결과

- T세포 → 클러스터 0번, 5번, 6번
- 대식세포 → 클러스터 2번, 4번
- 암세포 → 클러스터 7번, 9번
- B세포 → 클러스터 3번

⇒ 기준은 각 세포의 발현량이 보라색이 아닌 청록 계열로 보이는 경우

#### 반만 칠해져 있는 경우

T세포의 5번 6번 클러스터는 보라색이 반, 청록색이 반이다.
이럴 경우는 보류 한다. → 추후 데이터 왜곡의 가능성이 있다

⇒ **애매한 클러스터는 Unknown 으로 둔다**

```python
cell_type_map = {
    '0': 'T cell',
    '2': 'Macrophage',
    '4': 'Macrophage',
    '3': 'B cell',
    '7': 'Cancer cell',
    '9': 'Cancer cell',
}

adata.obs['cell_type'] = adata.obs['leiden'].map(cell_type_map).fillna('Unknown')
sc.pl.umap(adata, color='cell_type')
```

- 어노테이션을 적용하여 각 클러스터에 이름을 붙여준다
- 이름을 붙이지 않은 클러스터는 자동으로 Unknown으로 들어간다

![image.png](attachment:43bbdfa3-9242-4ccb-b452-ed480e79fc74:image.png)

#### 최종 전처리 결과 (phase 1 기준)

- B cell (파랑)
- T cell (빨강)
- Macrophage (초록)
- Cancer cell (주황)
- Unknown (보라) — 나중에 Phase 2에서 더 세분화

*26.05.10- 커밋 완료*

### ***Phase 1 종료***