from pathlib import Path
import xarray as xr


# ============================================================
# RUTES DEL PROJECTE
# ============================================================

# Ruta arrel del projecte:
# global-sst-anomaly-3d/
ROOT = Path(__file__).resolve().parents[1]

# Carpeta on guardarem les dades originals
DATA_RAW = ROOT / "data" / "raw"

# La cream si no existeix
DATA_RAW.mkdir(parents=True, exist_ok=True)

print("Carpeta de dades:", DATA_RAW)


# ============================================================
# 1. SST MITJANA - SETEMBRE 2026
# ============================================================

fitxer_sep2026 = DATA_RAW / "sst_sep2026.nc"

if fitxer_sep2026.exists():

    print("\n====================================")
    print("SST SETEMBRE 2026")
    print("====================================")

    print("El fitxer ja existeix:")
    print(fitxer_sep2026)

else:

    URL_MONTHLY = (
        "https://psl.noaa.gov/thredds/dodsC/"
        "Datasets/noaa.oisst.v2.highres/sst.mon.mean.nc"
    )

    print("\n====================================")
    print("SST SETEMBRE 2026")
    print("====================================")

    print("\nObrint dataset mensual NOAA OISST...")

    ds = xr.open_dataset(URL_MONTHLY)

    print(ds)

    # Seleccionam setembre de 2026
    sst_sep2026 = ds["sst"].sel(time="2026-09-01")

    print("\nSST setembre 2026:")
    print(sst_sep2026)

    # Carregam només aquesta capa des del servidor
    print("\nCarregant SST de setembre de 2026...")

    sst_sep2026 = sst_sep2026.load()

    # Guardam el resultat
    sst_sep2026.to_netcdf(fitxer_sep2026)

    print("\nFitxer guardat:")
    print(fitxer_sep2026)

    # Tancam el dataset remot
    ds.close()


# ============================================================
# 2. CLIMATOLOGIA SST - SETEMBRE 1991-2020
# ============================================================

fitxer_clim_sep = DATA_RAW / "sst_clim_sep_1991-2020.nc"

if fitxer_clim_sep.exists():

    print("\n====================================")
    print("CLIMATOLOGIA SST 1991-2020")
    print("====================================")

    print("El fitxer ja existeix:")
    print(fitxer_clim_sep)

else:

    URL_CLIM = (
        "https://psl.noaa.gov/thredds/dodsC/"
        "Datasets/noaa.oisst.v2.highres/"
        "sst.mon.ltm.1991-2020.nc"
    )

    print("\n====================================")
    print("CLIMATOLOGIA SST 1991-2020")
    print("====================================")

    print("\nObrint climatologia NOAA OISST 1991-2020...")

    # decode_times=False evita l'avís causat per les dates
    # fictícies de l'any 0001 del fitxer climatològic.
    ds_clim = xr.open_dataset(
        URL_CLIM,
        decode_times=False
    )

    print(ds_clim)

    # Els mesos estan ordenats:
    # 0 = gener
    # 1 = febrer
    # ...
    # 8 = setembre
    sst_clim_sep = ds_clim["sst"].isel(time=8)

    print("\nClimatologia SST de setembre 1991-2020:")
    print(sst_clim_sep)

    # Carregam només setembre
    print("\nCarregant climatologia de setembre 1991-2020...")

    sst_clim_sep = sst_clim_sep.load()

    # Guardam
    sst_clim_sep.to_netcdf(fitxer_clim_sep)

    print("\nFitxer guardat:")
    print(fitxer_clim_sep)

    # Tancam el dataset remot
    ds_clim.close()


# ============================================================
# 3. CONCENTRACIÓ DE GEL MARÍ - DATASET MENSUAL
# ============================================================

URL_ICE_MONTHLY = (
    "https://psl.noaa.gov/thredds/dodsC/"
    "Datasets/noaa.oisst.v2.highres/icec.mon.mean.nc"
)

print("\n====================================")
print("CONCENTRACIÓ DE GEL MARÍ")
print("====================================")

print("\nObrint dataset mensual de concentració de gel marí...")

ds_ice = xr.open_dataset(URL_ICE_MONTHLY)

print(ds_ice)

# ============================================================
# 4. GEL MARÍ - SETEMBRE 2026
# ============================================================

ice_sep2026 = ds_ice["icec"].sel(time="2026-09-01")

print("\nConcentració de gel marí - setembre 2026:")
print(ice_sep2026)

print("\nAtributs de la variable:")
print(ice_sep2026.attrs)

# ============================================================
# 5. GUARDAM GEL MARÍ - SETEMBRE 2026
# ============================================================

fitxer_ice_sep2026 = DATA_RAW / "ice_sep2026.nc"

if fitxer_ice_sep2026.exists():

    print("\nEl fitxer de gel marí setembre 2026 ja existeix:")
    print(fitxer_ice_sep2026)

else:

    print("\nCarregant gel marí de setembre 2026...")

    ice_sep2026 = ice_sep2026.load()

    ice_sep2026.to_netcdf(fitxer_ice_sep2026)

    print("Fitxer guardat:")
    print(fitxer_ice_sep2026)


# ============================================================
# 6. CLIMATOLOGIA DE GEL MARÍ 1991-2020
# ============================================================

URL_ICE_CLIM = (
    "https://psl.noaa.gov/thredds/dodsC/"
    "Datasets/noaa.oisst.v2.highres/"
    "icec.mon.ltm.1991-2020.nc"
)

print("\n====================================")
print("CLIMATOLOGIA DE GEL MARÍ 1991-2020")
print("====================================")

print("\nObrint climatologia de gel marí...")

ds_ice_clim = xr.open_dataset(
    URL_ICE_CLIM,
    decode_times=False
)

print(ds_ice_clim)

# ============================================================
# 7. SELECCIONAM SETEMBRE DE LA CLIMATOLOGIA DE GEL
# ============================================================

ice_clim_sep = ds_ice_clim["icec"].isel(time=8)

print("\nClimatologia de gel marí - setembre 1991-2020:")
print(ice_clim_sep)


# ============================================================
# 8. GUARDAM CLIMATOLOGIA DE GEL - SETEMBRE
# ============================================================

fitxer_ice_clim_sep = DATA_RAW / "ice_clim_sep_1991-2020.nc"

if fitxer_ice_clim_sep.exists():

    print("\nEl fitxer de climatologia de gel ja existeix:")
    print(fitxer_ice_clim_sep)

else:

    print("\nCarregant climatologia de gel de setembre 1991-2020...")

    ice_clim_sep = ice_clim_sep.load()

    ice_clim_sep.to_netcdf(fitxer_ice_clim_sep)

    print("Fitxer guardat:")
    print(fitxer_ice_clim_sep)


# Tancam els datasets remots
ds_ice.close()
ds_ice_clim.close()

print("\n====================================")
print("DESCÀRREGA COMPLETADA")
print("====================================")

print("\nFitxers disponibles a data/raw:")
print(" - sst_sep2026.nc")
print(" - sst_clim_sep_1991-2020.nc")
print(" - ice_sep2026.nc")
print(" - ice_clim_sep_1991-2020.nc")