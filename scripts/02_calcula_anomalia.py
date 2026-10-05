

from pathlib import Path
import numpy as np
import xarray as xr


# ============================================================
# RUTES DEL PROJECTE
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


# ============================================================
# OBRIM ELS DOS FITXERS
# ============================================================

fitxer_sep2026 = DATA_RAW / "sst_sep2026.nc"
fitxer_clim = DATA_RAW / "sst_clim_sep_1991-2020.nc"

print("Obrint SST setembre 2026...")
ds_sep2026 = xr.open_dataset(fitxer_sep2026)

print("Obrint climatologia setembre 1991-2020...")
ds_clim = xr.open_dataset(
    fitxer_clim,
    decode_times=False
)


print("\nSST setembre 2026:")
print(ds_sep2026)

print("\nClimatologia setembre:")
print(ds_clim)

# ============================================================
# COMPROVAM LES GRAELLES
# ============================================================

mateixes_latituds = np.array_equal(
    ds_sep2026["lat"].values,
    ds_clim["lat"].values
)

mateixes_longituds = np.array_equal(
    ds_sep2026["lon"].values,
    ds_clim["lon"].values
)

print("\n====================================")
print("COMPROVACIÓ DE GRAELLES")
print("====================================")

print("Mateixes latituds:", mateixes_latituds)
print("Mateixes longituds:", mateixes_longituds)

print(
    "Dimensions setembre 2026:",
    ds_sep2026["sst"].shape
)

print(
    "Dimensions climatologia:",
    ds_clim["sst"].shape
)

# ============================================================
# CALCULAM L'ANOMALIA DE SST
# ============================================================

sst_sep2026 = ds_sep2026["sst"]
sst_clim = ds_clim["sst"]

sst_anomalia = sst_sep2026 - sst_clim

sst_anomalia.name = "sst_anomaly"

sst_anomalia.attrs["long_name"] = (
    "Sea Surface Temperature anomaly - September 2026 "
    "relative to 1991-2020 climatology"
)
sst_anomalia.attrs["units"] = "degC"

print("\n====================================")
print("ANOMALIA SST")
print("====================================")

print(sst_anomalia)

print(
    "\nMínim:",
    float(sst_anomalia.min(skipna=True)),
    "°C"
)

print(
    "Màxim:",
    float(sst_anomalia.max(skipna=True)),
    "°C"
)

print(
    "Mitjana simple:",
    float(sst_anomalia.mean(skipna=True)),
    "°C"
)

# ============================================================
# LOCALITZAM ELS EXTREMS
# ============================================================

# Convertim l'anomalia a array NumPy
anom_values = sst_anomalia.values

# Índex del màxim i mínim ignorant NaN
idx_max = np.unravel_index(
    np.nanargmax(anom_values),
    anom_values.shape
)

idx_min = np.unravel_index(
    np.nanargmin(anom_values),
    anom_values.shape
)


# ============================================================
# MÀXIM
# ============================================================

ilat_max, ilon_max = idx_max

lat_max = float(sst_anomalia["lat"].values[ilat_max])
lon_max = float(sst_anomalia["lon"].values[ilon_max])

anom_max = float(
    sst_anomalia.isel(
        lat=ilat_max,
        lon=ilon_max
    )
)

sst2026_max = float(
    sst_sep2026.isel(
        lat=ilat_max,
        lon=ilon_max
    )
)

clim_max = float(
    sst_clim.isel(
        lat=ilat_max,
        lon=ilon_max
    )
)


# ============================================================
# MÍNIM
# ============================================================

ilat_min, ilon_min = idx_min

lat_min = float(sst_anomalia["lat"].values[ilat_min])
lon_min = float(sst_anomalia["lon"].values[ilon_min])

anom_min = float(
    sst_anomalia.isel(
        lat=ilat_min,
        lon=ilon_min
    )
)

sst2026_min = float(
    sst_sep2026.isel(
        lat=ilat_min,
        lon=ilon_min
    )
)

clim_min = float(
    sst_clim.isel(
        lat=ilat_min,
        lon=ilon_min
    )
)


# ============================================================
# MOSTRAM ELS RESULTATS
# ============================================================

print("\n====================================")
print("EXTREMS DE L'ANOMALIA")
print("====================================")

print("\nMÀXIM:")
print(f"Latitud:      {lat_max:.3f}°")
print(f"Longitud:     {lon_max:.3f}°")
print(f"SST 2026:     {sst2026_max:.2f} °C")
print(f"Climatologia: {clim_max:.2f} °C")
print(f"Anomalia:     {anom_max:.2f} °C")

print("\nMÍNIM:")
print(f"Latitud:      {lat_min:.3f}°")
print(f"Longitud:     {lon_min:.3f}°")
print(f"SST 2026:     {sst2026_min:.2f} °C")
print(f"Climatologia: {clim_min:.2f} °C")
print(f"Anomalia:     {anom_min:.2f} °C")


# ============================================================
# GEL MARÍ ALS PUNTS EXTREMS
# ============================================================

fitxer_ice_2026 = DATA_RAW / "ice_sep2026.nc"
fitxer_ice_clim = DATA_RAW / "ice_clim_sep_1991-2020.nc"

print("\nObrint dades de gel marí...")

ds_ice_2026 = xr.open_dataset(fitxer_ice_2026)
ds_ice_clim = xr.open_dataset(
    fitxer_ice_clim,
    decode_times=False
)

ice_2026 = ds_ice_2026["icec"]
ice_clim = ds_ice_clim["icec"]


# Comprovam que la graella coincideix
print("\n====================================")
print("COMPROVACIÓ GRAELLA GEL MARÍ")
print("====================================")

print(
    "Mateixes latituds:",
    np.array_equal(
        ice_2026["lat"].values,
        sst_anomalia["lat"].values
    )
)

print(
    "Mateixes longituds:",
    np.array_equal(
        ice_2026["lon"].values,
        sst_anomalia["lon"].values
    )
)


# ============================================================
# GEL AL PUNT D'ANOMALIA MÀXIMA
# ============================================================

ice2026_max = float(
    ice_2026.isel(
        lat=ilat_max,
        lon=ilon_max
    )
)

iceclim_max = float(
    ice_clim.isel(
        lat=ilat_max,
        lon=ilon_max
    )
)


# ============================================================
# GEL AL PUNT D'ANOMALIA MÍNIMA
# ============================================================

ice2026_min = float(
    ice_2026.isel(
        lat=ilat_min,
        lon=ilon_min
    )
)

iceclim_min = float(
    ice_clim.isel(
        lat=ilat_min,
        lon=ilon_min
    )
)


# ============================================================
# MOSTRAM RESULTATS
# ============================================================

print("\n====================================")
print("GEL MARÍ ALS EXTREMS")
print("====================================")

print("\nPUNT DE MÀXIMA ANOMALIA:")
print(f"Anomalia SST:        {anom_max:.2f} °C")
print(f"Gel setembre 2026:   {ice2026_max * 100:.1f} %")
print(f"Gel climatològic:    {iceclim_max * 100:.1f} %")

print("\nPUNT DE MÍNIMA ANOMALIA:")
print(f"Anomalia SST:        {anom_min:.2f} °C")
print(f"Gel setembre 2026:   {ice2026_min * 100:.1f} %")
print(f"Gel climatològic:    {iceclim_min * 100:.1f} %")

# ============================================================
# MÀSCARA DE GEL MARÍ
# ============================================================

# En OISST, les zones oceàniques sense gel poden aparèixer
# com NaN a icec. Només les interpretam com a 0 quan tenim
# SST vàlida en aquella mateixa cel·la.

ice_2026_ocean = ice_2026.fillna(0).where(
    sst_sep2026.notnull()
)

ice_clim_ocean = ice_clim.fillna(0).where(
    sst_clim.notnull()
)


# Llindar de concentració de gel
ICE_THRESHOLD = 0.15


# Cel·les influenciades pel gel en 2026 o en la climatologia
mascara_gel = (
    (ice_2026_ocean >= ICE_THRESHOLD)
    |
    (ice_clim_ocean >= ICE_THRESHOLD)
)


# Conservam només oceà obert comparable
sst_anomalia_ocean = sst_anomalia.where(~mascara_gel)

sst_anomalia_ocean.name = "sst_anomaly"

sst_anomalia_ocean.attrs["long_name"] = (
    "Sea Surface Temperature anomaly - September 2026 "
    "relative to 1991-2020 climatology, excluding sea-ice regions"
)

sst_anomalia_ocean.attrs["units"] = "degC"
sst_anomalia_ocean.attrs["sea_ice_threshold"] = "15 %"


print("\n====================================")
print("ANOMALIA SENSE ZONES DE GEL")
print("====================================")

print(
    "Mínim:",
    float(sst_anomalia_ocean.min(skipna=True)),
    "°C"
)

print(
    "Màxim:",
    float(sst_anomalia_ocean.max(skipna=True)),
    "°C"
)

print(
    "Mitjana simple:",
    float(sst_anomalia_ocean.mean(skipna=True)),
    "°C"
)

print(
    "Cel·les excloses per gel:",
    int(mascara_gel.sum(skipna=True))
)

# ============================================================
# EXTREMS DESPRÉS DE LA MÀSCARA DE GEL
# ============================================================

anom_ocean_values = sst_anomalia_ocean.values

idx_max_ocean = np.unravel_index(
    np.nanargmax(anom_ocean_values),
    anom_ocean_values.shape
)

idx_min_ocean = np.unravel_index(
    np.nanargmin(anom_ocean_values),
    anom_ocean_values.shape
)

ilat_max_ocean, ilon_max_ocean = idx_max_ocean
ilat_min_ocean, ilon_min_ocean = idx_min_ocean


# Màxim
lat_max_ocean = float(
    sst_anomalia_ocean["lat"].values[ilat_max_ocean]
)

lon_max_ocean = float(
    sst_anomalia_ocean["lon"].values[ilon_max_ocean]
)

anom_max_ocean = float(
    sst_anomalia_ocean.isel(
        lat=ilat_max_ocean,
        lon=ilon_max_ocean
    )
)

sst2026_max_ocean = float(
    sst_sep2026.isel(
        lat=ilat_max_ocean,
        lon=ilon_max_ocean
    )
)

clim_max_ocean = float(
    sst_clim.isel(
        lat=ilat_max_ocean,
        lon=ilon_max_ocean
    )
)

ice2026_max_ocean = float(
    ice_2026_ocean.isel(
        lat=ilat_max_ocean,
        lon=ilon_max_ocean
    )
)

iceclim_max_ocean = float(
    ice_clim_ocean.isel(
        lat=ilat_max_ocean,
        lon=ilon_max_ocean
    )
)


# Mínim
lat_min_ocean = float(
    sst_anomalia_ocean["lat"].values[ilat_min_ocean]
)

lon_min_ocean = float(
    sst_anomalia_ocean["lon"].values[ilon_min_ocean]
)

anom_min_ocean = float(
    sst_anomalia_ocean.isel(
        lat=ilat_min_ocean,
        lon=ilon_min_ocean
    )
)

sst2026_min_ocean = float(
    sst_sep2026.isel(
        lat=ilat_min_ocean,
        lon=ilon_min_ocean
    )
)

clim_min_ocean = float(
    sst_clim.isel(
        lat=ilat_min_ocean,
        lon=ilon_min_ocean
    )
)

ice2026_min_ocean = float(
    ice_2026_ocean.isel(
        lat=ilat_min_ocean,
        lon=ilon_min_ocean
    )
)

iceclim_min_ocean = float(
    ice_clim_ocean.isel(
        lat=ilat_min_ocean,
        lon=ilon_min_ocean
    )
)


print("\n====================================")
print("EXTREMS DESPRÉS DE LA MÀSCARA")
print("====================================")

print("\nMÀXIM:")
print(f"Latitud:       {lat_max_ocean:.3f}°")
print(f"Longitud:      {lon_max_ocean:.3f}°")
print(f"SST 2026:      {sst2026_max_ocean:.2f} °C")
print(f"Climatologia:  {clim_max_ocean:.2f} °C")
print(f"Anomalia:      {anom_max_ocean:.2f} °C")
print(f"Gel 2026:      {ice2026_max_ocean * 100:.1f} %")
print(f"Gel clim.:      {iceclim_max_ocean * 100:.1f} %")

print("\nMÍNIM:")
print(f"Latitud:       {lat_min_ocean:.3f}°")
print(f"Longitud:      {lon_min_ocean:.3f}°")
print(f"SST 2026:      {sst2026_min_ocean:.2f} °C")
print(f"Climatologia:  {clim_min_ocean:.2f} °C")
print(f"Anomalia:      {anom_min_ocean:.2f} °C")
print(f"Gel 2026:      {ice2026_min_ocean * 100:.1f} %")
print(f"Gel clim.:      {iceclim_min_ocean * 100:.1f} %")


# ============================================================
# ENTORN DEL MÀXIM DESPRÉS DE LA MÀSCARA
# ============================================================

# Agafam +/- 4 cel·les:
# 4 x 0.25° = 1° aproximadament
RADI = 4

i0 = max(0, ilat_max_ocean - RADI)
i1 = min(sst_anomalia.sizes["lat"], ilat_max_ocean + RADI + 1)

j0 = max(0, ilon_max_ocean - RADI)
j1 = min(sst_anomalia.sizes["lon"], ilon_max_ocean + RADI + 1)


anom_entorn = sst_anomalia.isel(
    lat=slice(i0, i1),
    lon=slice(j0, j1)
)

ice_clim_entorn = ice_clim_ocean.isel(
    lat=slice(i0, i1),
    lon=slice(j0, j1)
)

ice_2026_entorn = ice_2026_ocean.isel(
    lat=slice(i0, i1),
    lon=slice(j0, j1)
)


print("\n====================================")
print("ENTORN DEL MÀXIM (+/- 1 grau)")
print("====================================")

print("\nANOMALIA SST:")
print(
    np.round(
        anom_entorn.values,
        2
    )
)

print("\nGEL CLIMATOLÒGIC (%):")
print(
    np.round(
        ice_clim_entorn.values * 100,
        1
    )
)

print("\nGEL SETEMBRE 2026 (%):")
print(
    np.round(
        ice_2026_entorn.values * 100,
        1
    )
)


# ============================================================
# MITJANA GLOBAL PONDERADA PER ÀREA
# ============================================================

# Pes proporcional a l'àrea de cada cel·la de latitud
pesos_lat = np.cos(
    np.deg2rad(sst_anomalia["lat"])
)

# Mitjana global de l'anomalia completa
mitjana_global_raw = sst_anomalia.weighted(
    pesos_lat
).mean(
    dim=("lat", "lon"),
    skipna=True
)

# Mitjana global només sobre oceà obert comparable
mitjana_global_ocean = sst_anomalia_ocean.weighted(
    pesos_lat
).mean(
    dim=("lat", "lon"),
    skipna=True
)

print("\n====================================")
print("MITJANES GLOBALS PONDERADES")
print("====================================")

print(
    f"Anomalia global completa: "
    f"{float(mitjana_global_raw):.3f} °C"
)

print(
    f"Anomalia global oceà obert: "
    f"{float(mitjana_global_ocean):.3f} °C"
)

# ============================================================
# PREPARAM LES VARIABLES PER GUARDAR
# ============================================================

def preparar_variable(da):
    """
    Elimina la coordenada temporal escalar i els encodings
    heretats dels fitxers NOAA que poden causar conflictes
    en tornar a guardar el NetCDF.
    """

    da = da.drop_vars("time", errors="ignore").copy()

    # Eliminam informació d'encoding heretada
    da.encoding = {}

    # Per seguretat, eliminam també possibles atributs
    # relacionats amb valors absents.
    da.attrs.pop("_FillValue", None)
    da.attrs.pop("missing_value", None)

    return da


sst_sep2026_out = preparar_variable(
    sst_sep2026
)

sst_clim_out = preparar_variable(
    sst_clim
)

sst_anomalia_out = preparar_variable(
    sst_anomalia
)

sst_anomalia_ocean_out = preparar_variable(
    sst_anomalia_ocean
)

ice_2026_out = preparar_variable(
    ice_2026_ocean
)

ice_clim_out = preparar_variable(
    ice_clim_ocean
)

# La màscara la guardam com 0/1 en lloc de booleà
mascara_gel_out = preparar_variable(
    mascara_gel.astype("int8")
)


# ============================================================
# CREAM EL DATASET PROCESSAT
# ============================================================

fitxer_sortida = (
    DATA_PROCESSED /
    "sst_anomaly_sep2026_vs_1991-2020.nc"
)

ds_sortida = xr.Dataset(
    {
        "sst_sep2026": sst_sep2026_out,
        "sst_climatology": sst_clim_out,
        "sst_anomaly_raw": sst_anomalia_out,
        "sst_anomaly_open_ocean": sst_anomalia_ocean_out,
        "sea_ice_sep2026": ice_2026_out,
        "sea_ice_climatology": ice_clim_out,
        "sea_ice_mask": mascara_gel_out,
    }
)


# ============================================================
# METADADES GENERALS
# ============================================================

ds_sortida.attrs = {
    "title": (
        "September 2026 global sea surface temperature anomaly"
    ),
    "description": (
        "September 2026 SST compared with the "
        "1991-2020 September climatology"
    ),
    "source": "NOAA OISST v2.1",
    "spatial_resolution": "0.25 degree",
    "target_period": "September 2026",
    "reference_period": "September climatology 1991-2020",
    "sea_ice_threshold": "0.15 (15%)",
    "global_mean_anomaly_raw_degC": float(
        mitjana_global_raw
    ),
    "global_mean_anomaly_open_ocean_degC": float(
        mitjana_global_ocean
    ),
}


# ============================================================
# METADADES DE VARIABLES
# ============================================================

ds_sortida["sst_sep2026"].attrs = {
    "long_name": (
        "Mean sea surface temperature - September 2026"
    ),
    "units": "degC",
}

ds_sortida["sst_climatology"].attrs = {
    "long_name": (
        "Mean September sea surface temperature "
        "climatology 1991-2020"
    ),
    "units": "degC",
}

ds_sortida["sst_anomaly_raw"].attrs = {
    "long_name": (
        "September 2026 SST anomaly relative to "
        "1991-2020 September climatology"
    ),
    "units": "degC",
}

ds_sortida["sst_anomaly_open_ocean"].attrs = {
    "long_name": (
        "September 2026 SST anomaly excluding "
        "sea-ice-influenced regions"
    ),
    "units": "degC",
}

ds_sortida["sea_ice_sep2026"].attrs = {
    "long_name": (
        "Sea ice concentration - September 2026"
    ),
    "units": "fraction",
}

ds_sortida["sea_ice_climatology"].attrs = {
    "long_name": (
        "September sea ice concentration climatology "
        "1991-2020"
    ),
    "units": "fraction",
}

ds_sortida["sea_ice_mask"].attrs = {
    "long_name": (
        "Mask for sea-ice-influenced grid cells"
    ),
    "criterion": (
        "Sea ice concentration >= 15% in September 2026 "
        "or in the 1991-2020 September climatology"
    ),
    "values": "0 = retained, 1 = sea-ice influenced",
}


# ============================================================
# ENCODING DEL NOSTRE FITXER
# ============================================================

encoding = {
    "sst_sep2026": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sst_climatology": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sst_anomaly_raw": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sst_anomaly_open_ocean": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sea_ice_sep2026": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sea_ice_climatology": {
        "dtype": "float32",
        "_FillValue": np.nan,
        "zlib": True,
        "complevel": 4,
    },
    "sea_ice_mask": {
        "dtype": "int8",
        "zlib": True,
        "complevel": 4,
    },
}


# ============================================================
# GUARDAM
# ============================================================

ds_sortida.to_netcdf(
    fitxer_sortida,
    encoding=encoding
)

print("\n====================================")
print("FITXER PROCESSAT GUARDAT")
print("====================================")

print(fitxer_sortida)

print("\nDataset final:")
print(ds_sortida)