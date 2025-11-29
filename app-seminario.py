import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

# --- 1. Configuração da Página e Estilo (CSS) ---
st.set_page_config(
    page_title="Lei de Gauss | Seminário",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400;700&display=swap');

    .stApp {
        background-color: #050511;
        font-family: 'Roboto Mono', monospace;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0b0c1a;
        border-right: 1px solid #1f2937;
    }
    
    h1, h2, h3 {
        color: #00f2ff !important;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
    }
    
    div[data-testid="stMetric"] {
        background-color: #111322;
        border: 1px solid #00f2ff;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
    }
    label[data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.4rem !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #111322;
        border-radius: 4px;
        color: white;
        border: 1px solid #333;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00f2ff !important;
        color: black !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Cabeçalho ---
col_head1, col_head2 = st.columns([0.1, 0.9])
with col_head1:
    st.markdown("<h1 style='text-align: center;'>⚡</h1>", unsafe_allow_html=True)
with col_head2:
    st.title("Simulador: Lei de Gauss")
    st.caption("Visualização interativa de Campos e Potenciais em Cascas Esféricas")

st.markdown("---")

# --- 3. Barra Lateral (Controles) ---
with st.sidebar:
    st.title("🎛️ Painel de Controle")
    
    with st.expander("🌐 Geometria da Casca", expanded=True):
        R = st.slider("Raio (R)", 0.5, 3.0, 1.5, 0.1, help="Raio da esfera condutora em metros")
    
    with st.expander("⚡ Carga Elétrica", expanded=True):
        Q = st.slider("Carga Total (Q)", -10.0, 10.0, 5.0, 0.5, help="Carga em nanoCoulombs")
        
    with st.expander("⚙️ Visualização"):
        res = st.select_slider("Qualidade (Resolução)", options=[30, 50, 80], value=50)
        show_vectors = st.toggle("Vetores de Campo", value=True)
    
    st.info("💡 **Dica:** O gráfico é interativo. Use o mouse para zoom e rotação.")
    st.markdown("Desenvolvido para **Física III**")

# --- 4. Physics Engine (NumPy) ---
k = 9e9
L = 4.0
x = np.linspace(-L, L, res)
y = np.linspace(-L, L, res)
X, Y = np.meshgrid(x, y)
Dist = np.sqrt(X**2 + Y**2)

E_mag = np.zeros_like(Dist)
V_pot = np.zeros_like(Dist)
Ex = np.zeros_like(Dist)
Ey = np.zeros_like(Dist)

mask_inside = Dist < R
mask_outside = Dist >= R

r_safe = np.where(Dist == 0, 1e-9, Dist) 

# Cálculos
E_mag[mask_outside] = k * abs(Q) / (r_safe[mask_outside]**2)
V_pot[mask_outside] = k * Q / r_safe[mask_outside]

Ex[mask_outside] = E_mag[mask_outside] * (X[mask_outside] / r_safe[mask_outside]) * np.sign(Q)
Ey[mask_outside] = E_mag[mask_outside] * (Y[mask_outside] / r_safe[mask_outside]) * np.sign(Q)

E_mag[mask_inside] = 0
V_pot[mask_inside] = k * Q / R

limit_val = np.percentile(E_mag, 98) if np.any(mask_outside) else 1.0
E_mag = np.clip(E_mag, 0, limit_val)

# --- 5. Visualização Principal ---

tab1, tab2 = st.tabs(["VISÃO 2D (CAMPO)", "VISÃO 3D (POTENCIAL)"])

with tab1:
    col_main, col_metrics = st.columns([3, 1])
    
    with col_metrics:
        st.markdown("### 📊 Dados em Tempo Real")
        
        E_sup = (k * abs(Q)) / (R**2)
        
        st.metric("Campo na Superfície (r=R)", f"{E_sup:.2e} N/C")
        st.metric("Potencial Interno (r<R)", f"{(k*Q/R):.2e} V")
        
        st.markdown("---")
        if abs(Q) > 0:
            fluxo = "Positivo (Saindo)" if Q > 0 else "Negativo (Entrando)"
            cor_fluxo = "green" if Q > 0 else "red"
            st.markdown(f"**Fluxo:** :{cor_fluxo}[{fluxo}]")
        else:
            st.markdown("**Fluxo:** Nulo")

    with col_main:
        fig2d = go.Figure()
        
        # Heatmap
        fig2d.add_trace(go.Heatmap(
            z=E_mag, x=x, y=y,
            colorscale='Inferno',
            zmin=0, zmax=limit_val,
            colorbar=dict(
                title=dict(text='|E| (N/C)', font=dict(color='white')), 
                tickfont=dict(color='white')
            ),
            hoverinfo='z'
        ))

        # Círculo
        fig2d.add_shape(type="circle",
            xref="x", yref="y",
            x0=-R, y0=-R, x1=R, y1=R,
            line=dict(color="#00f2ff", width=4),
        )

        # Vetores
        step = 2
        if show_vectors and Q != 0:
            quiver = ff.create_quiver(
                X[::step, ::step], Y[::step, ::step],
                Ex[::step, ::step], Ey[::step, ::step],
                scale=0.25/np.mean(E_mag[mask_outside]) if np.any(mask_outside) else 1,
                arrow_scale=0.3,
                line_color='rgba(255, 255, 255, 0.4)'
            )
            fig2d.add_traces(quiver.data)

        # Layout CORRIGIDO (Removidos parâmetros legacy que causavam erro)
        fig2d.update_layout(
            title=dict(text="Magnitude do Campo Elétrico", font=dict(color="white")),
            xaxis=dict(
                title=dict(text="X (m)", font=dict(color='white')), 
                constrain="domain", 
                showgrid=False, 
                zeroline=False, 
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                title=dict(text="Y (m)", font=dict(color='white')), 
                scaleanchor="x", 
                scaleratio=1,
                showgrid=False, 
                zeroline=False, 
                tickfont=dict(color='white')
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            autosize=True
        )
        st.plotly_chart(fig2d, use_container_width=True)

with tab2:
    st.markdown("### Topologia do Potencial")
    
    fig3d = go.Figure(data=[go.Surface(
        z=V_pot, x=x, y=y,
        colorscale='Viridis',
        opacity=0.9,
        colorbar=dict(
            title=dict(text='Volts', font=dict(color='white')),
            tickfont=dict(color='white')
        )
    )])

    # Layout 3D CORRIGIDO
    fig3d.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text='X', font=dict(color='white')),
                showgrid=True, 
                gridcolor='#333', 
                zerolinecolor='#333', 
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                title=dict(text='Y', font=dict(color='white')),
                showgrid=True, 
                gridcolor='#333', 
                zerolinecolor='#333', 
                tickfont=dict(color='white')
            ),
            zaxis=dict(
                title=dict(text='V', font=dict(color='white')),
                showgrid=True, 
                gridcolor='#333', 
                zerolinecolor='#333', 
                tickfont=dict(color='white')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    st.plotly_chart(fig3d, use_container_width=True)

# --- 6. Rodapé Teórico ---
with st.expander("📚 Explicar a Física por trás disso (Cola para o Seminário)"):
    st.markdown(r"""
    A **Lei de Gauss** afirma que o fluxo elétrico total através de uma superfície fechada é proporcional à carga contida.
    
    $$ \oint \vec{E} \cdot d\vec{A} = \frac{Q_{int}}{\epsilon_0} $$
    
    Na simulação (simetria esférica):
    1.  **Dentro ($r < R$):** Não há carga encapsulada ($Q_{int} = 0$). Logo, $E = 0$. O potencial é constante.
    2.  **Fora ($r \ge R$):** A casca se comporta como uma carga pontual no centro. $E = \frac{kQ}{r^2}$.
    """)