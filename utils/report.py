"""
Validation helper

각 단계가 끝날 때마다 >>adata<< 내부 구조를 확인한다
목적은 “코드가 실행됐다”가 아니라 >>데이터가 의도한 구조로 변했는지 검증<<하는 것이다

"""


def ph1_report_adata_state(adata, step_name: str, show_keys: bool = True):
    """AnnData의 핵심 상태를 단계별로 출력한다."""
    print(f"\n===== {step_name} =====")
    print(f"shape: {adata.n_obs:,} cells × {adata.n_vars:,} genes")
    print(f"X type: {type(adata.X)}")
    print(f"X dtype: {getattr(adata.X, 'dtype', 'N/A')}")
    print(f"obs names unique: {adata.obs_names.is_unique}")
    print(f"var names unique: {adata.var_names.is_unique}")
    if show_keys:
        print(f"obs columns: {list(adata.obs.columns)[:12]}{' ...' if len(adata.obs.columns) > 12 else ''}")
        print(f"var columns: {list(adata.var.columns)[:12]}{' ...' if len(adata.var.columns) > 12 else ''}")
        print(f"obsm keys: {list(adata.obsm.keys())}")
        print(f"obsp keys: {list(adata.obsp.keys())}")
        print(f"layers keys: {list(adata.layers.keys())}")
        print(f"uns keys: {list(adata.uns.keys())[:12]}{' ...' if len(adata.uns.keys()) > 12 else ''}")
        
        
        
def ph2_report_adata_state(adata, label):
    print(f"===== {label} =====")
    print(f"shape: {adata.n_obs:,} cells x {adata.n_vars:,} genes")
    print(f"X type: {type(adata.X)}")
    print(f"X dtype: {getattr(adata.X, 'dtype', 'NA')}")
    print(f"obs names unique: {adata.obs_names.is_unique}")
    print(f"var names unique: {adata.var_names.is_unique}")
    print(f"obs columns: {list(adata.obs.columns)}")
    print(f"obsm keys: {list(adata.obsm.keys())}")
    print(f"obsp keys: {list(adata.obsp.keys())}")
    print(f"layers keys: {list(adata.layers.keys())}")
    print(f"uns keys: {list(adata.uns.keys())}")
    print()