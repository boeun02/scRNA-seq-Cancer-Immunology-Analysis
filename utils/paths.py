from pathlib import Path

BASE_DIR = Path('..') / 'dataset' / 'raw'
DATA_DIR = BASE_DIR / 'GSE127465_RAW'
H5AD_PATH = BASE_DIR / 'GSE127465_human_all.h5ad'

SAVE_DIR = Path('..') / 'dataset'
HUMAN_H5AD = SAVE_DIR / 'GSE127465_human_final.h5ad'

MAC_SUB_H5AD = SAVE_DIR / 'GSE127465_mac_subtyped.h5ad'
MAC_PH2_H5AD = SAVE_DIR / 'GSE127465_mac_phase2a.h5ad'
MAC_TME_H5AD = SAVE_DIR / 'GSE127465_mac_phase2a_tme.h5ad'