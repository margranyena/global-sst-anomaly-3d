
from pathlib import Path
import json

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from matplotlib.colors import (
    TwoSlopeNorm,
    LinearSegmentedColormap
)


# ============================================================
# RUTES DEL PROJECTE
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_PROCESSED = ROOT / "data" / "processed"

DOCS = ROOT / "docs"
GLOBE = DOCS / "globe"
ASSETS = GLOBE / "assets"

DOCS.mkdir(parents=True, exist_ok=True)
GLOBE.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

# ============================================================
# OBRIM EL DATASET PROCESSAT
# ============================================================

fitxer = (
    DATA_PROCESSED /
    "sst_anomaly_sep2026_vs_1991-2020.nc"
)

print("Obrint dataset processat...")

ds = xr.open_dataset(fitxer)

anomalia = ds["sst_anomaly_raw"]

mascara_gel = (
    ds["sea_ice_mask"]
    .astype(bool)
)


print("\nDimensions originals:")
print(
    anomalia.sizes["lat"],
    "x",
    anomalia.sizes["lon"]
)

print(
    "\nMínim:",
    float(anomalia.min(skipna=True)),
    "°C"
)

print(
    "Màxim:",
    float(anomalia.max(skipna=True)),
    "°C"
)


# ============================================================
# ESCALA DE COLORS
# ============================================================

VMIN = -4.0
VMAX = 6.5

norm = TwoSlopeNorm(
    vmin=VMIN,
    vcenter=0.0,
    vmax=VMAX
)


# ============================================================
# COLORMAP
# ============================================================

# Exactament la mateixa lògica que al mapa 2D:
#
# negatius:
# blau -> cian -> blanc
#
# 0 a 2:
# blanc -> groc -> taronja
#
# 2 a 4:
# taronja -> vermell intens
#
# 4 a 6.5:
# vermell intens -> negre

colors = [

    # Negatius
    (norm(-4.0), "#1D0066"),
    (norm(-3.0), "#0000CC"),
    (norm(-2.0), "#0066FF"),
    (norm(-1.0), "#00CCFF"),
    (norm(-0.5), "#A6E7FF"),

    # Zero
    (norm(0.0), "#FFFFFF"),

    # 0 -> 2
    (norm(1.0), "#FFF066"),
    (norm(2.0), "#FFB000"),

    # 2 -> 4
    (norm(3.0), "#FF5A00"),
    (norm(4.0), "#E00000"),

    # 4 -> 6.5
    (norm(5.0), "#8A0000"),
    (norm(6.0), "#2A0000"),
    (norm(6.5), "#000000"),
]


cmap = LinearSegmentedColormap.from_list(
    "sst_anomaly_globe",
    colors
)

cmap.set_under("#12004A")
cmap.set_over("#000000")


# ============================================================
# CONVERTIM EL CAMP EN UNA TEXTURA RGBA
# ============================================================

valors = anomalia.values

rgba = cmap(
    norm(valors)
)


# ============================================================
# TERRA FERMA
# ============================================================

# A OISST les cel·les terrestres apareixen
# principalment com NaN.

terra = np.isnan(valors)

rgba[terra] = [
    0.72,
    0.72,
    0.72,
    1.00
]


# ============================================================
# ZONES DE GEL MARÍ
# ============================================================

# Mateixa filosofia que al mapa 2D:
# mostram un puntejat discret, no una màscara completa.

PAS_GEL = 6

gel = mascara_gel.values

files, columnes = np.indices(
    gel.shape
)

punts_gel = (
    gel
    & (files % PAS_GEL == 0)
    & (columnes % PAS_GEL == 0)
)

rgba[punts_gel] = [
    0.0,
    0.0,
    0.0,
    1.0
]


# ============================================================
# ORIENTACIÓ DE LA TEXTURA
# ============================================================

# El NetCDF està ordenat:
# sud -> nord
#
# Una textura equirectangular estàndard necessita:
# nord -> sud

rgba = np.flipud(rgba)


# ============================================================
# GUARDAM LA TEXTURA
# ============================================================

fitxer_textura = (
    ASSETS /
    "sst_anomaly_sep2026_texture.png"
)

plt.imsave(
    fitxer_textura,
    rgba
)


print("\n====================================")
print("TEXTURA GUARDADA")
print("====================================")

print(fitxer_textura)

print(
    "Resolució:",
    rgba.shape[1],
    "x",
    rgba.shape[0],
    "píxels"
)


# ============================================================
# GUARDAM LES DADES NUMÈRIQUES PER AL HOVER
# ============================================================

# Per més endavant poder clicar / passar el ratolí
# sobre el globus i recuperar el valor real.

anomalia_web = np.where(
    np.isfinite(valors),
    valors,
    np.nan
).astype(np.float32)

fitxer_valors = (
    ASSETS /
    "sst_anomaly_values.npy"
)

np.save(
    fitxer_valors,
    anomalia_web
)
# ============================================================
# VERSIÓ BINÀRIA PER A JAVASCRIPT
# ============================================================

fitxer_valors_bin = (
    ASSETS /
    "sst_anomaly_values.bin"
)

anomalia_web.tofile(
    fitxer_valors_bin
)

print("\nValors binaris per a la web guardats:")
print(fitxer_valors_bin)

print("\nValors numèrics guardats:")
print(fitxer_valors)


# ============================================================
# METADADES
# ============================================================

metadata = {

    "title": (
        "Global Sea Surface Temperature Anomaly "
        "— September 2026"
    ),

    "source": "NOAA OISST v2.1",

    "target_period": "September 2026",

    "reference_period": (
        "1991-2020 September climatology"
    ),

    "resolution_degrees": 0.25,

    "n_lat": int(
        anomalia.sizes["lat"]
    ),

    "n_lon": int(
        anomalia.sizes["lon"]
    ),

    "texture_width": int(
        rgba.shape[1]
    ),

    "texture_height": int(
        rgba.shape[0]
    ),

    "color_min_degC": VMIN,

    "color_max_degC": VMAX,

    "data_min_degC": float(
        anomalia.min(skipna=True)
    ),

    "data_max_degC": float(
        anomalia.max(skipna=True)
    ),

    "global_mean_anomaly_degC": float(
        ds.attrs[
            "global_mean_anomaly_raw_degC"
        ]
    ),

    "global_mean_open_ocean_degC": float(
        ds.attrs[
            "global_mean_anomaly_open_ocean_degC"
        ]
    ),

    "longitude_min": float(
        anomalia["lon"].min()
    ),

    "longitude_max": float(
        anomalia["lon"].max()
    ),

    "latitude_min": float(
        anomalia["lat"].min()
    ),

    "latitude_max": float(
        anomalia["lat"].max()
    ),
}


fitxer_metadata = (
    ASSETS /
    "metadata.json"
)

with open(
    fitxer_metadata,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\nMetadades guardades:")
print(fitxer_metadata)

# ============================================================
# TEXTURA DE COSTES
# ============================================================

# Terra = punts NaN de l'anomalia
land = np.isnan(anomalia.values)
ocean = ~land

# Detectam la frontera terra-mar
ocean_n = np.zeros_like(ocean)
ocean_n[1:, :] = ocean[:-1, :]

ocean_s = np.zeros_like(ocean)
ocean_s[:-1, :] = ocean[1:, :]

ocean_w = np.roll(ocean, 1, axis=1)
ocean_e = np.roll(ocean, -1, axis=1)

land_n = np.zeros_like(land)
land_n[1:, :] = land[:-1, :]

land_s = np.zeros_like(land)
land_s[:-1, :] = land[1:, :]

land_w = np.roll(land, 1, axis=1)
land_e = np.roll(land, -1, axis=1)

coast = (
    land & (ocean_n | ocean_s | ocean_w | ocean_e)
)

coast_thick = coast.copy()

# PNG transparent amb línia negra
coast_rgba = np.zeros(
    (
        anomalia.sizes["lat"],
        anomalia.sizes["lon"],
        4
    ),
    dtype=np.uint8
)

coast_rgba[coast_thick] = [0, 0, 0, 255]

# Nord a dalt, igual que la textura principal
coast_rgba = np.flipud(coast_rgba)

fitxer_coast = (
    ASSETS /
    "coastline_overlay.png"
)

plt.imsave(
    fitxer_coast,
    coast_rgba
)

print("\nTextura de costes guardada:")
print(fitxer_coast)

# ============================================================
# TANCAM EL DATASET
# ============================================================

ds.close()


# ============================================================
# FINAL
# ============================================================

print("\n====================================")
print("PREPARACIÓ DEL GLOBUS COMPLETADA")
print("====================================")

print("\nFitxers creats:")

print(
    " -",
    fitxer_textura
)

print(
    " -",
    fitxer_valors
)

print(
    " -",
    fitxer_metadata
)