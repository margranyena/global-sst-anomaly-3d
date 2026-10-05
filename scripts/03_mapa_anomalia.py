
from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

import cartopy.crs as ccrs
import cartopy.feature as cfeature


# ============================================================
# RUTES DEL PROJECTE
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)


# ============================================================
# OBRIM EL DATASET PROCESSAT
# ============================================================

fitxer = (
    DATA_PROCESSED /
    "sst_anomaly_sep2026_vs_1991-2020.nc"
)

print("Obrint dataset processat...")

ds = xr.open_dataset(fitxer)

print(ds)


# ============================================================
# VARIABLES
# ============================================================

anomalia_raw = ds["sst_anomaly_raw"]
anomalia_ocean = ds["sst_anomaly_open_ocean"]
mascara_gel = ds["sea_ice_mask"].astype(bool)


# ============================================================
# ESCALA DEL MAPA
# ============================================================

VMIN = -4.0
VMAX = 6.5

norm = TwoSlopeNorm(
    vmin=VMIN,
    vcenter=0.0,
    vmax=VMAX
)


# ============================================================
# COLORMAP PERSONALITZAT
# ============================================================

colors = [
    # Part negativa
    (norm(-4.0), "#1D0066"),
    (norm(-3.0), "#0000CC"),
    (norm(-2.0), "#0066FF"),
    (norm(-1.0), "#00CCFF"),
    (norm(-0.5), "#A6E7FF"),
    (norm( 0.0), "#FFFFFF"),

    # 0 a 2: blanc -> groc -> taronja
    (norm( 1.0), "#FFF066"),
    (norm( 2.0), "#FFB000"),

    # 2 a 4: taronja -> vermell intens
    (norm( 3.0), "#FF5A00"),
    (norm( 4.0), "#E00000"),

    # 4 a 6.5: vermell intens -> negre
    (norm( 5.0), "#8A0000"),
    (norm( 6.0), "#2A0000"),
    (norm( 6.5), "#000000"),
]

cmap = LinearSegmentedColormap.from_list(
    "sst_anomaly_black_end",
    colors
)

cmap.set_under("#12004A")
cmap.set_over("#000000")


# ============================================================
# COMPROVACIÓ DE L'ESCALA
# ============================================================

exces_calid = (
    (anomalia_raw > VMAX)
    & (~mascara_gel)
)

exces_fred = (
    (anomalia_raw < VMIN)
    & (~mascara_gel)
)

n_calid = int(exces_calid.sum())
n_fred = int(exces_fred.sum())

max_ocean = float(anomalia_ocean.max(skipna=True))
min_ocean = float(anomalia_ocean.min(skipna=True))

print("\n====================================")
print("COMPROVACIÓ DE L'ESCALA")
print("====================================")
print(f"Cel·les > +{VMAX} °C fora de zones de gel:", n_calid)
print(f"Cel·les < {VMIN} °C fora de zones de gel:", n_fred)
print("Màxim fora de zones de gel:", max_ocean, "°C")
print("Mínim fora de zones de gel:", min_ocean, "°C")


# ============================================================
# CREAM LA FIGURA
# ============================================================

fig = plt.figure(figsize=(16, 8))

# Mapa ovalat estil "bonic" amb projecció Robinson
ax = fig.add_axes(
    [0.04, 0.18, 0.92, 0.68],
    projection=ccrs.Robinson(
        central_longitude=180
    )
)

ax.set_global()


# ============================================================
# ANOMALIA DE SST
# ============================================================

mapa = ax.pcolormesh(
    anomalia_raw["lon"],
    anomalia_raw["lat"],
    anomalia_raw,
    transform=ccrs.PlateCarree(),
    cmap=cmap,
    norm=norm,
    shading="auto",
    zorder=1
)


# ============================================================
# ZONES INFLUÏDES PEL GEL MARÍ
# ============================================================

PAS = 6

lon2d, lat2d = np.meshgrid(
    mascara_gel["lon"].values,
    mascara_gel["lat"].values
)

mask_plot = mascara_gel.values

lon_sub = lon2d[::PAS, ::PAS]
lat_sub = lat2d[::PAS, ::PAS]
mask_sub = mask_plot[::PAS, ::PAS]

ax.scatter(
    lon_sub[mask_sub],
    lat_sub[mask_sub],
    s=0.7,
    c="black",
    alpha=0.16,
    transform=ccrs.PlateCarree(),
    zorder=6,
)


# ============================================================
# CONTINENTS I COSTES
# ============================================================

ax.add_feature(
    cfeature.LAND,
    facecolor="lightgray",
    zorder=10
)

ax.coastlines(
    linewidth=0.65,
    zorder=11
)


# ============================================================
# GRAELLA GEOGRÀFICA
# ============================================================

gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=False,
    linewidth=0.35,
    color="gray",
    alpha=0.25,
    linestyle="--"
)


# ============================================================
# CONTORN DEL MAPA
# ============================================================

ax.spines["geo"].set_linewidth(1.0)
ax.spines["geo"].set_edgecolor("black")

# ============================================================
# TÍTOL
# ============================================================

ax.set_title(
    "Global Sea Surface Temperature Anomaly — September 2026\n"
    "Relative to 1991–2020 September climatology | NOAA OISST v2.1",
    fontsize=14,
    pad=14
)




# ============================================================
# BARRA DE COLORS
# ============================================================

cax = fig.add_axes(
    [0.14, 0.10, 0.72, 0.032]
)

cbar = fig.colorbar(
    mapa,
    cax=cax,
    orientation="horizontal",
    extend="both",
    ticks=[
        -4, -3, -2, -1, 0,
         1,  2,  3,  4,  5,  6, 6.5
    ]
)

cbar.set_label(
    "Sea Surface Temperature anomaly (°C)",
    fontsize=11
)


# ============================================================
# GUARDAM LA FIGURA
# ============================================================

fitxer_figura = (
    FIGURES /
    "sst_anomaly_global_sep2026_robinson.png"
)

plt.savefig(
    fitxer_figura,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.06
)

print("\n====================================")
print("FIGURA GUARDADA")
print("====================================")
print(fitxer_figura)


# ============================================================
# MOSTRAM EL MAPA
# ============================================================

plt.show()


# ============================================================
# TANCAM EL DATASET
# ============================================================

ds.close()