import logging
from pathlib import Path
from data_processing import carregar_dados_regiao
from visualization import (
    plot_distribuicao_temperatura, plot_serie_temporal,
    plot_media_movel, plot_variacao_diaria, plot_heatmap_semanal,
    plot_comparacao_regioes, plot_correlacao_temperatura_hora,
    plot_extremos_temperatura, plot_comparacao_estados,
    plot_mapa_calor_estados, plot_serie_temporal_estados,
    plot_estatisticas_estados,
    # Novas funções de visualização
    plot_radar_estado_capital, plot_violino_estado_capital,
    plot_ciclo_diario_estado_capital, plot_calor_horario_estado_capital,
    plot_densidade_estado_capital, plot_boxen_estado_capital,
    plot_regressao_estado_capital, plot_barras_estado_capital,
    plot_area_estado_capital, plot_polar_estado_capital
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

def carregar_dados_estado_capital(regiao, estado):
    """Carrega e combina dados do estado e sua capital"""
    try:
        pasta_dados = Path('data/raw')
        
        # Carregar dados do estado
        arquivo_estado = pasta_dados / f'INMET_{regiao}_UF_{estado}_2024.CSV'
        if arquivo_estado.exists():
            df_estado = pd.read_csv(arquivo_estado, sep=';')
            df_estado['TIPO'] = 'ESTADO'
            df_estado['DATA'] = pd.to_datetime(df_estado['DATA'])
            df_estado = adicionar_colunas_tempo(df_estado)
        else:
            logger.warning(f"Arquivo não encontrado para o estado {estado}")
            return None
            
        # Carregar dados da capital
        arquivo_capital = pasta_dados / f'INMET_{regiao}_UF_{estado}_CAPITAL_2024.CSV'
        if arquivo_capital.exists():
            df_capital = pd.read_csv(arquivo_capital, sep=';')
            df_capital['TIPO'] = 'CAPITAL'
            df_capital['DATA'] = pd.to_datetime(df_capital['DATA'])
            df_capital = adicionar_colunas_tempo(df_capital)
        else:
            logger.warning(f"Arquivo não encontrado para a capital de {estado}")
            return None
            
        # Combinar dados
        df_combinado = pd.concat([df_estado, df_capital], ignore_index=True)
        return df_combinado
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados de {estado}: {str(e)}")
        return None

def adicionar_colunas_tempo(df):
    """Adiciona colunas de hora e dia da semana ao DataFrame"""
    df['HORA'] = df['DATA'].dt.hour
    df['DIA_SEMANA'] = df['DATA'].dt.day_name()
    return df

def main():
    # Criar diretório reports se não existir
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    logger.info("Diretório reports criado/verificado com sucesso")
    
    # Lista de regiões
    regioes = ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']
    
    # Carregar dados de todas as regiões
    dados_regioes = {}
    for regiao in regioes:
        df = carregar_dados_regiao(regiao)
        if df is not None:
            dados_regioes[regiao] = df
    
    logger.info(f"Dados carregados para {len(dados_regioes)} regiões")
    
    # Gerar visualizações individuais por região
    for regiao, df in dados_regioes.items():
        logger.info(f"Gerando visualizações para {regiao}")
        
        # Visualizações básicas
        plot_distribuicao_temperatura(df, regiao, reports_dir)
        plot_serie_temporal(df, regiao, reports_dir)
        plot_media_movel(df, regiao, reports_dir)
        plot_variacao_diaria(df, regiao, reports_dir)
        plot_heatmap_semanal(df, regiao, reports_dir)
        plot_correlacao_temperatura_hora(df, regiao, reports_dir)
        plot_extremos_temperatura(df, regiao, reports_dir)
        
        # Visualizações por estado
        plot_serie_temporal_estados(df, regiao, reports_dir)
    
    # Gerar visualizações comparativas entre regiões e estados
    if len(dados_regioes) > 1:
        plot_comparacao_regioes(dados_regioes, reports_dir)
        plot_comparacao_estados(dados_regioes, reports_dir)
        plot_mapa_calor_estados(dados_regioes, reports_dir)
        plot_estatisticas_estados(dados_regioes, reports_dir)

    # Lista de regiões e estados
    estados = {
        'SUDESTE': ['SP', 'RJ'],
        'SUL': ['PR', 'SC']
    }
    
    # Gerar visualizações por estado e capital
    for regiao, lista_estados in estados.items():
        for estado in lista_estados:
            logger.info(f"Gerando visualizações para {estado}")
            
            # Carregar dados combinados do estado e capital
            df_combinado = carregar_dados_estado_capital(regiao, estado)
            
            if df_combinado is not None:
                # Gerar as 10 novas visualizações
                plot_radar_estado_capital(df_combinado, estado, reports_dir)
                plot_violino_estado_capital(df_combinado, estado, reports_dir)
                plot_ciclo_diario_estado_capital(df_combinado, estado, reports_dir)
                plot_calor_horario_estado_capital(df_combinado, estado, reports_dir)
                plot_densidade_estado_capital(df_combinado, estado, reports_dir)
                plot_boxen_estado_capital(df_combinado, estado, reports_dir)
                plot_regressao_estado_capital(df_combinado, estado, reports_dir)
                plot_barras_estado_capital(df_combinado, estado, reports_dir)
                plot_area_estado_capital(df_combinado, estado, reports_dir)
                plot_polar_estado_capital(df_combinado, estado, reports_dir)
            else:
                logger.warning(f"Não foi possível gerar visualizações para {estado}")

if __name__ == '__main__':
    main()
