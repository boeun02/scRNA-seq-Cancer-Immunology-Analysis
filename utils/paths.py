from pathlib import Path

BASE_DIR = Path('.') / 'dataset' / 'raw'
DATA_DIR = BASE_DIR / 'GSE127465_RAW'
H5AD_PATH = BASE_DIR / 'GSE127465_human_all.h5ad'

SAVE_DIR = Path('.') / 'dataset'
HUMAN_H5AD = SAVE_DIR / 'GSE127465_human_final.h5ad'

MAC_SUB_H5AD = SAVE_DIR / 'GSE127465_mac_subtyped.h5ad'
MAC_PH2_H5AD = SAVE_DIR / 'GSE127465_mac_phase2a.h5ad'
MAC_TME_H5AD = SAVE_DIR / 'GSE127465_mac_phase2a_tme.h5ad'

CSV_DIR = Path('.') / 'dataset' / 'phase2b'
LYM_META = CSV_DIR / 'GSE154763_LYM_metadata.csv.gz'
LYM_NM = CSV_DIR / 'GSE154763_LYM_normalized_expression.csv.gz'
LYM_H5AD = CSV_DIR / 'GSE154763_LYM.h5ad'

ALL_OUTER_H5AD = SAVE_DIR / 'GSE154763_all_outer.h5ad'
ALL_INNER_H5AD = SAVE_DIR / 'GSE154763_all_inner.h5ad'
ALL_MAC_H5AD = SAVE_DIR / 'GSE154763_all_mac.h5ad'
ALL_MAC_SCORE_H5AD = SAVE_DIR / 'GSE154763_all_mac_score.h5ad'