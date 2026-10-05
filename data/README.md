# Data

## Source

All data come from the **Kenneth R. French Data Library**
(<https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>),
constructed from the **August 2026 Bloomberg database**. The library is free
for research use; please cite French's data library when reusing.

## Files (vendored under `data/raw/` for reproducibility)

| File | Contents |
|------|----------|
| `Europe_5_Factors.csv` | Monthly European factors: Mkt-RF, SMB, HML, RMW, CMA, RF (Jul 1990 – Aug 2026) |
| `Europe_25_Portfolios_ME_BE-ME.csv` | Monthly returns of 25 value-weighted Size–B/M portfolios, Europe (Jul 1990 – Aug 2026) |

Missing values are coded as `-99.99` in the source files and treated as NaN
by `factorlab.data.loaders`.

## Refresh

To re-download the latest vintage:

```bash
python -m factorlab download Europe_5_Factors_CSV.zip Europe_25_Portfolios_ME_BE-ME_CSV.zip --dest data/raw
```

then re-run the study:

```bash
python -m factorlab run examples/europe_ff3_ff5/config.yaml
```

Note that results will change slightly as the library is updated each month.
