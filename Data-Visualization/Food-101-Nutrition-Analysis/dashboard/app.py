import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Análise Nutricional Food-101",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS minimalista
st.markdown("""
    <style>
    .main {
        padding: 0 1rem;
    }
    .stApp {
        background-color: #ffffff;
    }
    .block-container {
        padding-top: 1rem;
    }
    .stSidebar {
        background-color: #f8f9fa;
        padding: 1rem 0.5rem;
    }
    .stSidebar .block-container {
        padding: 0;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 0;
    }
    .filter-section {
        margin-bottom: 2rem;
        padding: 0.5rem;
    }
    .filter-section h3 {
        color: #2c3e50;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid #e9ecef;
    }
    .stButton button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Dicionários de tradução (mantido como está)
food_translations = {
    'apple_pie': 'Torta de Maçã',
    'baby_back_ribs': 'Costela Suína',
    'baklava': 'Baklava',
    'beef_carpaccio': 'Carpaccio de Carne',
    'beef_tartare': 'Carne Crua Temperada',
    'beet_salad': 'Salada de Beterraba',
    'beignets': 'Beignets',
    'bibimbap': 'Bibimbap',
    'bread_pudding': 'Pudim de Pão',
    'breakfast_burrito': 'Burrito de Café da Manhã',
    'bruschetta': 'Bruschetta',
    'caesar_salad': 'Salada Caesar',
    'cannoli': 'Cannoli',
    'caprese_salad': 'Salada Caprese',
    'carrot_cake': 'Bolo de Cenoura',
    'ceviche': 'Ceviche',
    'cheese_plate': 'Prato de Queijos',
    'cheesecake': 'Cheesecake',
    'chicken_curry': 'Frango ao Curry',
    'chicken_quesadilla': 'Quesadilla de Frango',
    'chicken_wings': 'Asinhas de Frango',
    'chocolate_cake': 'Bolo de Chocolate',
    'chocolate_mousse': 'Mousse de Chocolate',
    'churros': 'Churros',
    'clam_chowder': 'Sopa de Mariscos',
    'club_sandwich': 'Sanduíche Club',
    'crab_cakes': 'Bolinhos de Caranguejo',
    'creme_brulee': 'Creme Brulée',
    'croque_madame': 'Croque Madame',
    'cup_cakes': 'Cupcakes',
    'deviled_eggs': 'Ovos Recheados',
    'donuts': 'Donuts',
    'dumplings': 'Dumplings',
    'edamame': 'Edamame',
    'eggs_benedict': 'Ovos Benedict',
    'escargots': 'Escargots',
    'falafel': 'Falafel',
    'filet_mignon': 'Filé Mignon',
    'fish_and_chips': 'Peixe e Batatas Fritas',
    'foie_gras': 'Foie Gras',
    'french_fries': 'Batatas Fritas',
    'french_onion_soup': 'Sopa de Cebola',
    'french_toast': 'Rabanada',
    'fried_calamari': 'Lula Frita',
    'fried_rice': 'Arroz Frito',
    'frozen_yogurt': 'Iogurte Gelado',
    'garlic_bread': 'Pão de Alho',
    'gnocchi': 'Nhoque',
    'greek_salad': 'Salada Grega',
    'grilled_cheese_sandwich': 'Sanduíche de Queijo Grelhado',
    'grilled_salmon': 'Salmão Grelhado',
    'guacamole': 'Guacamole',
    'gyoza': 'Guioza',
    'hamburger': 'Hambúrguer',
    'hot_and_sour_soup': 'Sopa Ácida e Picante',
    'hot_dog': 'Cachorro-Quente',
    'huevos_rancheros': 'Ovos à Moda Rancho',
    'hummus': 'Homus',
    'ice_cream': 'Sorvete',
    'lasagna': 'Lasanha',
    'lobster_bisque': 'Sopa de Lagosta',
    'lobster_roll_sandwich': 'Sanduíche de Lagosta',
    'macaroni_and_cheese': 'Macarrão com Queijo',
    'macarons': 'Macarons',
    'miso_soup': 'Sopa Missô',
    'mussels': 'Mexilhões',
    'nachos': 'Nachos',
    'omelette': 'Omelete',
    'onion_rings': 'Anéis de Cebola',
    'oysters': 'Ostras',
    'pad_thai': 'Pad Thai',
    'paella': 'Paella',
    'pancakes': 'Panquecas',
    'panna_cotta': 'Panna Cotta',
    'peking_duck': 'Pato à Pequim',
    'pho': 'Pho',
    'pizza': 'Pizza',
    'pork_chop': 'Costeleta de Porco',
    'poutine': 'Poutine',
    'prime_rib': 'Costela Premium',
    'pulled_pork_sandwich': 'Sanduíche de Porco Desfiado',
    'ramen': 'Lámen',
    'ravioli': 'Ravióli',
    'red_velvet_cake': 'Bolo Red Velvet',
    'risotto': 'Risoto',
    'samosa': 'Samosa',
    'sashimi': 'Sashimi',
    'scallops': 'Vieiras',
    'seaweed_salad': 'Salada de Algas',
    'shrimp_and_grits': 'Camarão com Mingau de Milho',
    'spaghetti_bolognese': 'Espaguete à Bolonhesa',
    'spaghetti_carbonara': 'Espaguete à Carbonara',
    'spring_rolls': 'Rolinhos Primavera',
    'steak': 'Bife',
    'strawberry_shortcake': 'Bolo de Morango',
    'sushi': 'Sushi',
    'tacos': 'Tacos',
    'takoyaki': 'Takoyaki',
    'tiramisu': 'Tiramisu',
    'tuna_tartare': 'Tartare de Atum',
    'waffles': 'Waffles'
}

nutrient_names = {
    "calories": "Calorias",
    "protein": "Proteínas",
    "carbohydrates": "Carboidratos",
    "fats": "Gorduras",
    "fiber": "Fibras",
    "sugars": "Açúcares",
    "sodium": "Sódio"
}

# Load and cache data
@st.cache_data
def load_data():
    data_path = Path(__file__).parents[1] / "data" / "nutrition.csv"
    df = pd.read_csv(data_path)
    df = df.groupby('label').first().reset_index()
    
    # Traduzir nomes dos alimentos
    df['label_pt'] = df['label'].map(food_translations)
    
    # Calcular métricas de qualidade nutricional
    df['protein_density'] = (df['protein'] / df['calories'] * 100).round(2)
    df['fiber_density'] = (df['fiber'] / df['calories'] * 100).round(2)
    df['carb_density'] = (df['carbohydrates'] / df['calories'] * 100).round(2)
    
    # Score nutricional (0-100)
    max_values = {
        'protein_density': 20,  # 20g proteína por 100kcal é excelente
        'fiber_density': 10,    # 10g fibra por 100kcal é excelente
        'sugars': 25,          # Limite máximo de açúcar
        'sodium': 2300,        # Limite máximo de sódio
    }
    
    # Calcular scores individuais (0-100)
    df['protein_score'] = (df['protein_density'] / max_values['protein_density'] * 100).clip(0, 100)
    df['fiber_score'] = (df['fiber_density'] / max_values['fiber_density'] * 100).clip(0, 100)
    df['sugar_score'] = ((max_values['sugars'] - df['sugars']) / max_values['sugars'] * 100).clip(0, 100)
    df['sodium_score'] = ((max_values['sodium'] - df['sodium']) / max_values['sodium'] * 100).clip(0, 100)
    
    # Score final (prioriza proteína e fibra, penaliza açúcar e sódio)
    df['nutrition_score'] = (
        df['protein_score'] * 0.35 +
        df['fiber_score'] * 0.35 +
        df['sugar_score'] * 0.15 +
        df['sodium_score'] * 0.15
    ).round(1)
    
    # Classificar alimentos
    df['recomendacao'] = pd.qcut(
        df['nutrition_score'],
        q=4,
        labels=['Evitar', 'Consumo Moderado', 'Bom', 'Excelente']
    )
    
    # Categorizar por tipo principal de nutriente
    conditions = [
        (df['protein_density'] > 15),                    # Alto em proteína
        (df['fiber_density'] > 7),                       # Alto em fibra
        (df['fiber'] >= 6),                             # Rico em fibra (baseado em RDA)
        (df['carb_density'] > 50) & (df['fiber'] >= 4), # Rico em carboidratos complexos
        (df['sugars'] < 5),                             # Baixo açúcar
    ]
    choices = [
        'Rico em Proteína',
        'Alto em Fibra',
        'Rico em Fibra',
        'Rico em Carboidratos Complexos',
        'Baixo Açúcar'
    ]
    df['perfil_nutricional'] = np.select(conditions, choices, default='Balanceado')
    
    return df

# Load data
df = load_data()

# Sidebar com filtros
with st.sidebar:
    st.title("🔍 Filtros Nutricionais")
    
    # Filtro de recomendação
    st.subheader("Recomendação")
    opcoes_recomendacao = sorted(df['recomendacao'].unique())
    recomendacoes = st.multiselect(
        "Nível de Recomendação",
        options=opcoes_recomendacao,
        default=opcoes_recomendacao[:2]  # Seleciona os dois primeiros níveis
    )
    
    # Filtros de calorias
    st.subheader("Calorias")
    cal_max = st.slider(
        "Limite de Calorias (kcal)",
        min_value=int(df['calories'].min()),
        max_value=int(df['calories'].max()),
        value=500,
        help="Filtrar alimentos até este valor calórico"
    )
    
    # Perfil nutricional
    st.subheader("Perfil Nutricional")
    opcoes_perfil = sorted(df['perfil_nutricional'].unique())
    perfis = st.multiselect(
        "Tipo de Alimento",
        options=opcoes_perfil,
        default=opcoes_perfil[:2]  # Seleciona os dois primeiros perfis
    )
    
    # Filtros nutricionais específicos
    st.subheader("Nutrientes")
    col1, col2 = st.columns(2)
    
    with col1:
        min_protein = st.number_input(
            "Mín. Proteína (g)",
            min_value=0.0,
            max_value=float(df['protein'].max()),
            value=0.0,
            step=1.0
        )
        min_fiber = st.number_input(
            "Mín. Fibra (g)",
            min_value=0.0,
            max_value=float(df['fiber'].max()),
            value=0.0,
            step=1.0
        )
    
    with col2:
        max_sugar = st.number_input(
            "Máx. Açúcar (g)",
            min_value=0.0,
            max_value=float(df['sugars'].max()),
            value=float(df['sugars'].max()),
            step=1.0
        )
        max_sodium = st.number_input(
            "Máx. Sódio (mg)",
            min_value=0.0,
            max_value=float(df['sodium'].max()),
            value=float(df['sodium'].max()),
            step=100.0
        )

# Aplicar filtros
df_filtered = df.copy()  # Começar com todos os dados

# Aplicar filtros somente se foram selecionados
if recomendacoes:
    df_filtered = df_filtered[df_filtered['recomendacao'].isin(recomendacoes)]

if perfis:
    df_filtered = df_filtered[df_filtered['perfil_nutricional'].isin(perfis)]

# Aplicar demais filtros
df_filtered = df_filtered[
    (df_filtered['calories'] <= cal_max) &
    (df_filtered['protein'] >= min_protein) &
    (df_filtered['fiber'] >= min_fiber) &
    (df_filtered['sugars'] <= max_sugar) &
    (df_filtered['sodium'] <= max_sodium)
]

# Verificar se há resultados após filtros
if len(df_filtered) == 0:
    st.warning("Nenhum alimento encontrado com os filtros selecionados. Tente ajustar os critérios.")
    st.stop()

# Header principal
st.title("🥗 Guia Nutricional Food-101")

# Métricas principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Alimentos Selecionados", len(df_filtered))
with col2:
    st.metric("Média de Calorias", f"{df_filtered['calories'].mean():.0f} kcal")
with col3:
    st.metric("Score Nutricional Médio", f"{df_filtered['nutrition_score'].mean():.1f}/100")

# Melhores escolhas nutricionais
st.header("🏆 Melhores Escolhas por Perfil")

# Se nenhum perfil foi selecionado, mostrar todos
perfis_para_mostrar = perfis if perfis else sorted(df['perfil_nutricional'].unique())

# Agrupar por perfil nutricional
for perfil in perfis_para_mostrar:
    st.subheader(f"📌 {perfil}")
    df_perfil = df_filtered[df_filtered['perfil_nutricional'] == perfil]
    
    if len(df_perfil) > 0:
        # Top alimentos do perfil (até 5)
        top_n = min(5, len(df_perfil))
        top_foods = df_perfil.nlargest(top_n, 'nutrition_score')
        fig = px.bar(
            top_foods,
            x='nutrition_score',
            y='label_pt',
            orientation='h',
            color='calories',
            title=f'Top {top_n} Alimentos - {perfil}',
            labels={
                'nutrition_score': 'Score Nutricional',
                'label_pt': 'Alimento',
                'calories': 'Calorias'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

# Análise de Combinações Personalizadas
st.header("🤝 Análise de Combinações")

# Interface para seleção de alimentos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Primeiro Alimento")
    # Criar lista de opções com opção padrão
    opcoes_alimento1 = ["Selecione um alimento..."] + list(df_filtered['label_pt'].dropna().sort_values())
    alimento1 = st.selectbox(
        "Selecione o primeiro alimento",
        options=opcoes_alimento1,
        key='alimento1'
    )

with col2:
    st.subheader("Segundo Alimento")
    # Criar lista de opções com opção padrão
    if alimento1 and alimento1 != "Selecione um alimento...":
        opcoes_alimento2 = ["Selecione um alimento..."] + list(df_filtered[
            (df_filtered['label_pt'] != alimento1) & 
            (df_filtered['label_pt'].notna())
        ]['label_pt'].sort_values())
    else:
        opcoes_alimento2 = ["Selecione um alimento..."]
    
    alimento2 = st.selectbox(
        "Selecione o segundo alimento",
        options=opcoes_alimento2,
        key='alimento2'
    )

# Analisar combinação selecionada
if (alimento1 != "Selecione um alimento..." and 
    alimento2 != "Selecione um alimento..." and 
    alimento1 and alimento2):
    # Buscar dados dos alimentos selecionados
    item1 = df_filtered[df_filtered['label_pt'] == alimento1].iloc[0]
    item2 = df_filtered[df_filtered['label_pt'] == alimento2].iloc[0]
    
    # Calcular métricas da combinação
    calorias_total = item1['calories'] + item2['calories']
    proteina_total = item1['protein'] + item2['protein']
    fibra_total = item1['fiber'] + item2['fiber']
    score_medio = (item1['nutrition_score'] + item2['nutrition_score']) / 2
    
    # Mostrar análise da combinação
    st.subheader("📊 Análise da Combinação")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Calorias Totais", f"{calorias_total:.0f} kcal")
    with col2:
        st.metric("Proteína Total", f"{proteina_total:.1f}g")
    with col3:
        st.metric("Fibra Total", f"{fibra_total:.1f}g")
    with col4:
        st.metric("Score Médio", f"{score_medio:.1f}")
    
    # Detalhamento nutricional
    st.write("**Detalhamento por Alimento:**")
    
    # Criar DataFrame comparativo
    comparison_data = {
        'Alimento': [item1['label_pt'], item2['label_pt']],
        'Calorias': [item1['calories'], item2['calories']],
        'Proteína': [item1['protein'], item2['protein']],
        'Fibra': [item1['fiber'], item2['fiber']],
        'Açúcares': [item1['sugars'], item2['sugars']],
        'Sódio': [item1['sodium'], item2['sodium']],
        'Score': [item1['nutrition_score'], item2['nutrition_score']]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    # Gráfico comparativo
    fig = px.bar(
        df_comparison,
        x='Alimento',
        y=['Calorias', 'Proteína', 'Fibra', 'Açúcares'],
        title='Comparação Nutricional',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Avaliação da combinação
    st.subheader("💡 Avaliação da Combinação")
    
    # Análise calórica
    if calorias_total <= cal_max:
        st.success(f"✅ Combinação dentro do limite calórico ({cal_max} kcal)")
    else:
        st.warning(f"⚠️ Combinação excede o limite calórico ({cal_max} kcal)")
    
    # Análise proteica
    if proteina_total >= min_protein:
        st.success(f"✅ Atinge o mínimo de proteína desejado ({min_protein}g)")
    else:
        st.info(f"ℹ️ Abaixo do mínimo de proteína desejado ({min_protein}g)")
    
    # Análise de fibras
    if fibra_total >= min_fiber:
        st.success(f"✅ Atinge o mínimo de fibra desejado ({min_fiber}g)")
    else:
        st.info(f"ℹ️ Abaixo do mínimo de fibra desejado ({min_fiber}g)")
    
    # Score nutricional
    if score_medio >= 70:
        st.success("🌟 Excelente combinação nutricional!")
    elif score_medio >= 50:
        st.info("✨ Boa combinação nutricional")
    else:
        st.warning("⚠️ Combinação com potencial para melhorias")

# Tabela detalhada
st.header("📋 Detalhamento Nutricional")
if st.checkbox("Mostrar tabela completa"):
    cols_to_show = [
        'label_pt', 'calories', 'protein', 'fiber', 'sugars', 'sodium',
        'nutrition_score', 'perfil_nutricional', 'recomendacao'
    ]
    
    df_display = df_filtered[cols_to_show].copy()
    df_display.columns = [
        'Alimento', 'Calorias', 'Proteína (g)', 'Fibras (g)', 
        'Açúcares (g)', 'Sódio (mg)', 'Score', 'Perfil', 'Recomendação'
    ]
    
    df_display = df_display.sort_values('Score', ascending=False)
    
    st.dataframe(
        df_display.style.background_gradient(subset=['Score'], cmap='RdYlGn'),
        use_container_width=True
    )

# Guia de uso
st.header("ℹ️ Como Usar este Dashboard")
st.write("""
- **Score Nutricional**: Combina proteína, fibra, açúcar e sódio. Quanto maior, melhor.
- **Perfis Nutricionais**:
  - 🟢 Rico em Proteína: > 15g proteína por 100kcal
  - 🟡 Alto em Fibra: > 7g fibra por 100kcal
  - 🟣 Rico em Fibra: ≥6g fibra (baseado em RDA)
  - 🟣 Rico em Carboidratos Complexos: >50% calorias de carboidratos e ≥4g fibra
  - ⚪ Balanceado: Bom equilíbrio geral
- **Combinações**: Sugestões de pares de alimentos que se complementam nutricionalmente mantendo baixas calorias
""")
