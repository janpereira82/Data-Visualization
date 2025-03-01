"""
Módulo para processamento dos dados de temperatura e clima.
Contém funções para limpeza, transformação e preparação dos dados para análise.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import glob
import logging

logger = logging.getLogger(__name__)

def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados do arquivo CSV e realiza limpeza inicial.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo de dados
        
    Returns:
        pd.DataFrame: DataFrame com os dados limpos
    """
    try:
        df = pd.read_csv(caminho_arquivo)
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

def carregar_dados_regiao(regiao):
    """Carrega dados de temperatura para uma região específica"""
    try:
        pasta_dados = Path('data/raw')
        arquivos = list(pasta_dados.glob(f'INMET_{regiao}_*.CSV'))
        
        if not arquivos:
            logger.warning(f"Nenhum arquivo encontrado para a região {regiao}")
            return None
        
        logger.info(f"Carregando {len(arquivos)} arquivos para a região {regiao}")
        
        dfs = []
        for arquivo in arquivos:
            try:
                df = pd.read_csv(arquivo, sep=';')
                df['DATA'] = pd.to_datetime(df['DATA'])
                
                # Extrair estado do nome do arquivo se disponível
                nome_arquivo = arquivo.stem
                if '_UF_' in nome_arquivo:
                    estado = nome_arquivo.split('_UF_')[1].split('_')[0]
                    df['ESTADO'] = estado
                
                dfs.append(df)
            except Exception as e:
                logger.error(f"Erro ao carregar arquivo {arquivo}: {str(e)}")
        
        if dfs:
            df_final = pd.concat(dfs, ignore_index=True)
            df_final = adicionar_colunas_tempo(df_final)
            logger.info(f"Carregados {len(df_final)} registros para a região {regiao}")
            return df_final
        return None
    
    except Exception as e:
        logger.error(f"Erro ao carregar dados da região {regiao}: {str(e)}")
        return None

def adicionar_colunas_tempo(df):
    """Adiciona colunas de hora e dia da semana ao DataFrame"""
    try:
        df['HORA'] = df['DATA'].dt.hour
        df['DIA_SEMANA'] = df['DATA'].dt.day_name()
        return df
    except Exception as e:
        logger.error(f"Erro ao adicionar colunas de tempo: {str(e)}")
        return df

def preparar_dados(df):
    """Prepara os dados para análise"""
    if df is None:
        return None
        
    try:
        # Seleciona colunas relevantes
        df = df[['DATA', 'TEMPERATURA', 'REGIAO', 'ESTADO']]
        
        # Remove valores ausentes
        df = df.dropna()
        
        # Ordena por data
        df = df.sort_values('DATA')
        
        return df
        
    except Exception as e:
        logger.error(f"Erro ao preparar dados: {str(e)}")
        return None

def carregar_todas_regioes():
    """Carrega dados de todas as regiões"""
    regioes = ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']
    dados = {}
    
    for regiao in regioes:
        df = carregar_dados_regiao(regiao)
        if df is not None:
            dados[regiao] = preparar_dados(df)
    
    return dados

def preparar_dados_temperatura(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados de temperatura para análise.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados brutos
        
    Returns:
        pd.DataFrame: DataFrame processado
    """
    # Implementar lógica de preparação dos dados
    pass

def calcular_estatisticas_basicas(df: pd.DataFrame) -> dict:
    """
    Calcula estatísticas básicas dos dados.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        
    Returns:
        dict: Dicionário com estatísticas calculadas
    """
    # Implementar cálculos estatísticos
    pass
