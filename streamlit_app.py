import streamlit as st
import plotly.graph_objects as go

# ==========================================================
# KONFIGURASI
# ==========================================================

st.set_page_config(
    page_title="3D UV-Vis Spectrophotometer",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 3D UV-Vis Spectrophotometer")
st.caption("Simulasi interaktif alat spektrofotometer UV-Vis")

# ==========================================================
# SESSION STATE
# ==========================================================

if "open" not in st.session_state:
    st.session_state.open = False

if "component" not in st.session_state:
    st.session_state.component = None


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Kontrol Alat")

if st.sidebar.button("🔓 Buka Bagian Dalam", use_container_width=True):
    st.session_state.open = True

if st.sidebar.button("🔒 Tutup Alat", use_container_width=True):
    st.session_state.open = False

st.sidebar.divider()

st.sidebar.subheader("Komponen")

if st.sidebar.button("💡 Sumber Cahaya", use_container_width=True):
    st.session_state.open = True
    st.session_state.component = "light"

if st.sidebar.button("🌈 Monokromator", use_container_width=True):
    st.session_state.open = True
    st.session_state.component = "mono"

if st.sidebar.button("🧪 Kuvet", use_container_width=True):
    st.session_state.open = True
    st.session_state.component = "cuvette"

if st.sidebar.button("🔴 Detektor", use_container_width=True):
    st.session_state.open = True
    st.session_state.component = "detector"


# ==========================================================
# FUNGSI BALOK 3D
# ==========================================================

def add_box(
    fig,
    x0, x1,
    y0, y1,
    z0, z1,
    color,
    opacity=1,
    name=""
):

    x = [
        x0, x1, x1, x0,
        x0, x1, x1, x0
    ]

    y = [
        y0, y0, y1, y1,
        y0, y0, y1, y1
    ]

    z = [
        z0, z0, z0, z0,
        z1, z1, z1, z1
    ]

    faces = [
        (0, 1, 2),
        (0, 2, 3),
        (4, 5, 6),
        (4, 6, 7),
        (0, 1, 5),
        (0, 5, 4),
        (2, 3, 7),
        (2, 7, 6),
        (1, 2, 6),
        (1, 6, 5),
        (0, 3, 7),
        (0, 7, 4)
    ]

    i = [f[0] for f in faces]
    j = [f[1] for f in faces]
    k = [f[2] for f in faces]

    fig.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            color=color,
            opacity=opacity,
            name=name,
            hovertext=name,
            hoverinfo="text"
        )
    )


# ==========================================================
# MEMBUAT MODEL
# ==========================================================

fig = go.Figure()


# ==========================================================
# CASING UTAMA
# ==========================================================

casing_opacity = 0.18 if st.session_state.open else 1

add_box(
    fig,
    -6, 6,
    -3.5, 3.5,
    0, 4.5,
    "lightgray",
    casing_opacity,
    "Casing UV-Vis"
)


# ==========================================================
# ATAP
# ==========================================================

add_box(
    fig,
    -6.2, 6.2,
    -3.7, 3.7,
    4.5, 5,
    "gray",
    0.15 if st.session_state.open else 1,
    "Bagian atas"
)


# ==========================================================
# PANEL DEPAN
# ==========================================================

add_box(
    fig,
    -6, 6,
    -3.7, -3.4,
    0, 4.5,
    "dimgray",
    0.15 if st.session_state.open else 1,
    "Panel depan"
)


# ==========================================================
# LAYAR
# ==========================================================

add_box(
    fig,
    -4.5, -0.5,
    -3.95, -3.75,
    2, 3.8,
    "black",
    1,
    "Layar"
)

add_box(
    fig,
    -4.2, -0.8,
    -4.05, -3.95,
    2.25, 3.55,
    "deepskyblue",
    1,
    "Display UV-Vis"
)


# ==========================================================
# TOMBOL
# ==========================================================

button_positions = [
    (-4.0, 1.1),
    (-3.0, 1.1),
    (-2.0, 1.1),
    (-1.0, 1.1),
    (0.0, 1.1),
    (1.0, 1.1)
]

for x, z in button_positions:

    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[-4],
            z=[z],
            mode="markers",
            marker=dict(
                size=12,
                color="black"
            ),
            showlegend=False
        )
    )


# ==========================================================
# BAGIAN DALAM
# ==========================================================

if st.session_state.open:

    # ------------------------------------------------------
    # SUMBER CAHAYA
    # ------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=[-4.5],
            y=[0],
            z=[3],
            mode="markers+text",
            marker=dict(
                size=15,
                color="yellow"
            ),
            text=["Sumber Cahaya"],
            textposition="top center",
            name="Sumber Cahaya"
        )
    )


    # ------------------------------------------------------
    # MONOKROMATOR
    # ------------------------------------------------------

    add_box(
        fig,
        -3.5, -1.5,
        -1, 1,
        2, 4,
        "slategray",
        1,
        "Monokromator"
    )


    # ------------------------------------------------------
    # KUVET
    # ------------------------------------------------------

    add_box(
        fig,
        1.5, 3,
        -1, 1,
        2, 3,
        "cyan",
        0.65,
        "Kuvet"
    )


    # ------------------------------------------------------
    # DETEKTOR
    # ------------------------------------------------------

    fig.add_trace(
        go.Scatter3d(
            x=[4.5],
            y=[0],
            z=[2.5],
            mode="markers+text",
            marker=dict(
                size=16,
                color="red"
            ),
            text=["Detektor"],
            textposition="top center",
            name="Detektor"
        )
    )


    # ======================================================
    # JALUR CAHAYA
    # ======================================================

    fig.add_trace(
        go.Scatter3d(
            x=[
                -4.5,
                -2.5,
                2.2,
                4.5
            ],
            y=[0, 0, 0, 0],
            z=[3, 3, 2.5, 2.5],
            mode="lines",
            line=dict(
                color="yellow",
                width=10
            ),
            name="Jalur Cahaya"
        )
    )


# ==========================================================
# PENGATURAN 3D
# ==========================================================

fig.update_layout(

    scene=dict(

        xaxis=dict(
            title="Lebar",
            showgrid=False
        ),

        yaxis=dict(
            title="Kedalaman",
            showgrid=False
        ),

        zaxis=dict(
            title="Tinggi",
            showgrid=False
        ),

        aspectmode="manual",

        aspectratio=dict(
            x=1.6,
            y=1,
            z=0.8
        ),

        camera=dict(
            eye=dict(
                x=1.7,
                y=-1.8,
                z=1.3
            )
        )
    ),

    height=650,

    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0
    ),

    showlegend=False
)


# ==========================================================
# TAMPILKAN MODEL
# ==========================================================

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================================
# INFORMASI KOMPONEN
# ==========================================================

info = {

    "light": (
        "### 💡 Sumber Cahaya\n"
        "Menghasilkan radiasi UV dan cahaya tampak "
        "yang digunakan untuk menganalisis sampel."
    ),

    "mono": (
        "### 🌈 Monokromator\n"
        "Memilih panjang gelombang tertentu dari "
        "cahaya yang dihasilkan sumber."
    ),

    "cuvette": (
        "### 🧪 Kuvet\n"
        "Wadah sampel yang dilewati berkas cahaya "
        "sebelum mencapai detektor."
    ),

    "detector": (
        "### 🔴 Detektor\n"
        "Menangkap cahaya setelah melewati sampel "
        "dan mengubahnya menjadi sinyal listrik."
    )
}


if st.session_state.component:

    st.info(
        info[st.session_state.component]
    )


# ==========================================================
# PRINSIP KERJA
# ==========================================================

st.divider()

st.subheader("Prinsip Kerja UV-Vis")

st.markdown(
    """
    **Sumber cahaya → Monokromator → Kuvet/Sampel
    → Detektor → Hasil pengukuran**
    """
)
