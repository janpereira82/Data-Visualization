"""
Módulo para criação de visualizações dos dados de temperatura e clima.
Contém funções para gerar gráficos e visualizações interativas.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import logging

logger = logging.getLogger(__name__)

def configurar_estilo():
    """Configura o estilo dos gráficos"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12

def criar_diretorio_reports():
    """Cria o diretório reports se não existir"""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    return reports_dir

def salvar_grafico(plt, reports_dir, nome_arquivo, fechar=True):
    """Salva o gráfico com tratamento de erros"""
    try:
        plt.tight_layout()
        caminho = reports_dir / nome_arquivo
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        logger.info(f"Gráfico salvo em {caminho}")
        if fechar:
            plt.close()
    except Exception as e:
        logger.error(f"Erro ao salvar gráfico {nome_arquivo}: {str(e)}")

def plot_distribuicao_temperatura(df, regiao, reports_dir):
    """Gera gráfico de distribuição de temperatura para uma região"""
    try:
        configurar_estilo()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Boxplot
        sns.boxplot(data=df, y='TEMPERATURA', ax=ax1)
        ax1.set_title(f'Distribuição de Temperatura - {regiao}')
        ax1.set_ylabel('Temperatura (°C)')
        
        # Histograma
        sns.histplot(data=df, x='TEMPERATURA', kde=True, ax=ax2)
        ax2.set_title(f'Histograma de Temperatura - {regiao}')
        ax2.set_xlabel('Temperatura (°C)')
        
        salvar_grafico(plt, reports_dir, f'temp_distribuicao_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar gráfico de distribuição para {regiao}: {str(e)}")

def plot_serie_temporal(df, regiao, reports_dir):
    """Gera gráfico de série temporal para uma região"""
    try:
        configurar_estilo()
        plt.figure(figsize=(15, 6))
        
        sns.lineplot(data=df, x='DATA', y='TEMPERATURA')
        plt.title(f'Série Temporal de Temperatura - {regiao}')
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.xticks(rotation=45)
        
        salvar_grafico(plt, reports_dir, f'temp_temporal_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar série temporal para {regiao}: {str(e)}")

def plot_media_movel(df, regiao, reports_dir, janela=7):
    """Gera gráfico de média móvel para uma região"""
    try:
        configurar_estilo()
        plt.figure(figsize=(15, 6))
        
        df['MEDIA_MOVEL'] = df['TEMPERATURA'].rolling(window=janela, min_periods=1).mean()
        
        plt.plot(df['DATA'], df['TEMPERATURA'], alpha=0.5, label='Temperatura Diária')
        plt.plot(df['DATA'], df['MEDIA_MOVEL'], linewidth=2, label=f'Média Móvel ({janela} horas)')
        
        plt.title(f'Temperatura e Média Móvel - {regiao}')
        plt.xlabel('Data')
        plt.ylabel('Temperatura (°C)')
        plt.legend()
        plt.xticks(rotation=45)
        
        salvar_grafico(plt, reports_dir, f'temp_media_movel_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar média móvel para {regiao}: {str(e)}")

def plot_variacao_diaria(df, regiao, reports_dir):
    """Gera gráfico de variação diária de temperatura"""
    try:
        configurar_estilo()
        plt.figure(figsize=(12, 6))
        
        media_por_hora = df.groupby('HORA')['TEMPERATURA'].agg(['mean', 'std']).reset_index()
        
        plt.errorbar(
            media_por_hora['HORA'],
            media_por_hora['mean'],
            yerr=media_por_hora['std'],
            fmt='o-',
            capsize=5,
            label='Média ± Desvio Padrão'
        )
        
        plt.title(f'Variação Diária Média de Temperatura - {regiao}')
        plt.xlabel('Hora do Dia')
        plt.ylabel('Temperatura Média (°C)')
        plt.grid(True)
        plt.legend()
        
        salvar_grafico(plt, reports_dir, f'temp_variacao_diaria_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar variação diária para {regiao}: {str(e)}")

def plot_heatmap_semanal(df, regiao, reports_dir):
    """Gera heatmap de temperatura por dia da semana e hora"""
    try:
        configurar_estilo()
        plt.figure(figsize=(15, 8))
        
        pivot = df.pivot_table(
            values='TEMPERATURA',
            index='DIA_SEMANA',
            columns='HORA',
            aggfunc='mean'
        )
        
        sns.heatmap(pivot, cmap='RdYlBu_r', center=pivot.mean().mean(), annot=True, fmt='.1f')
        plt.title(f'Heatmap de Temperatura - {regiao}')
        plt.xlabel('Hora do Dia')
        plt.ylabel('Dia da Semana')
        
        salvar_grafico(plt, reports_dir, f'temp_heatmap_semanal_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar heatmap semanal para {regiao}: {str(e)}")

def plot_comparacao_regioes(dfs_dict, reports_dir):
    """Gera gráfico comparativo entre regiões"""
    try:
        configurar_estilo()
        plt.figure(figsize=(12, 8))
        
        # Preparar dados para o boxplot
        dados_combinados = pd.concat([
            pd.DataFrame({
                'Temperatura': df['TEMPERATURA'],
                'Região': regiao
            }) for regiao, df in dfs_dict.items()
        ])
        
        sns.boxplot(data=dados_combinados, x='Região', y='Temperatura')
        plt.title('Comparação de Temperatura entre Regiões')
        plt.xlabel('Região')
        plt.ylabel('Temperatura (°C)')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        salvar_grafico(plt, reports_dir, 'temp_comparacao_regioes.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar comparação entre regiões: {str(e)}")

def plot_correlacao_temperatura_hora(df, regiao, reports_dir):
    """Gera gráfico de correlação entre temperatura e hora do dia"""
    try:
        configurar_estilo()
        plt.figure(figsize=(10, 6))
        
        sns.regplot(data=df, x='HORA', y='TEMPERATURA', scatter_kws={'alpha':0.5})
        plt.title(f'Correlação Temperatura vs Hora do Dia - {regiao}')
        plt.xlabel('Hora do Dia')
        plt.ylabel('Temperatura (°C)')
        
        salvar_grafico(plt, reports_dir, f'temp_correlacao_hora_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar correlação temperatura-hora para {regiao}: {str(e)}")

def plot_extremos_temperatura(df, regiao, reports_dir):
    """Gera gráfico de valores extremos de temperatura"""
    try:
        configurar_estilo()
        plt.figure(figsize=(12, 6))
        
        p05 = np.percentile(df['TEMPERATURA'], 5)
        p95 = np.percentile(df['TEMPERATURA'], 95)
        
        sns.histplot(data=df, x='TEMPERATURA', bins=30)
        plt.axvline(p05, color='r', linestyle='--', label=f'Percentil 5% ({p05:.1f}°C)')
        plt.axvline(p95, color='r', linestyle='--', label=f'Percentil 95% ({p95:.1f}°C)')
        
        plt.title(f'Distribuição e Valores Extremos de Temperatura - {regiao}')
        plt.xlabel('Temperatura (°C)')
        plt.ylabel('Contagem')
        plt.legend()
        
        salvar_grafico(plt, reports_dir, f'temp_extremos_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar gráfico de extremos para {regiao}: {str(e)}")

def analise_estatistica(df):
    """Retorna análise estatística básica dos dados"""
    try:
        return {
            'média': df['TEMPERATURA'].mean(),
            'mediana': df['TEMPERATURA'].median(),
            'desvio_padrão': df['TEMPERATURA'].std(),
            'mínima': df['TEMPERATURA'].min(),
            'máxima': df['TEMPERATURA'].max(),
            'percentil_5': np.percentile(df['TEMPERATURA'], 5),
            'percentil_95': np.percentile(df['TEMPERATURA'], 95)
        }
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {str(e)}")
        return {}

def plot_comparacao_estados(dfs_dict, reports_dir):
    """Gera gráfico comparativo entre estados"""
    try:
        configurar_estilo()
        plt.figure(figsize=(15, 8))
        
        # Preparar dados para o boxplot
        dados_combinados = []
        for regiao, df in dfs_dict.items():
            if 'ESTADO' in df.columns:
                for estado in df['ESTADO'].unique():
                    dados_estado = df[df['ESTADO'] == estado]
                    dados_combinados.append(pd.DataFrame({
                        'Temperatura': dados_estado['TEMPERATURA'],
                        'Estado': estado,
                        'Região': regiao
                    }))
        
        if dados_combinados:
            dados_combinados = pd.concat(dados_combinados)
            
            sns.boxplot(data=dados_combinados, x='Estado', y='Temperatura', hue='Região')
            plt.title('Comparação de Temperatura entre Estados')
            plt.xlabel('Estado')
            plt.ylabel('Temperatura (°C)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend(title='Região')
            
            salvar_grafico(plt, reports_dir, 'temp_comparacao_estados.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar comparação entre estados: {str(e)}")

def plot_mapa_calor_estados(dfs_dict, reports_dir):
    """Gera mapa de calor das temperaturas médias por estado"""
    try:
        configurar_estilo()
        plt.figure(figsize=(15, 10))
        
        # Calcular médias por estado
        medias_estados = []
        for regiao, df in dfs_dict.items():
            if 'ESTADO' in df.columns:
                medias = df.groupby('ESTADO')['TEMPERATURA'].agg(['mean', 'std']).round(2)
                medias['Região'] = regiao
                medias_estados.append(medias)
        
        if medias_estados:
            medias_estados = pd.concat(medias_estados)
            
            pivot = medias_estados.pivot_table(
                values='mean',
                index='Região',
                columns=medias_estados.index,
                aggfunc='first'
            )
            
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlBu_r')
            plt.title('Temperatura Média por Estado')
            plt.xlabel('Estado')
            plt.ylabel('Região')
            
            salvar_grafico(plt, reports_dir, 'temp_mapa_calor_estados.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar mapa de calor dos estados: {str(e)}")

def plot_serie_temporal_estados(df, regiao, reports_dir):
    """Gera gráfico de série temporal para cada estado de uma região"""
    try:
        if 'ESTADO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(15, 8))
            
            for estado in df['ESTADO'].unique():
                dados_estado = df[df['ESTADO'] == estado]
                plt.plot(dados_estado['DATA'], dados_estado['TEMPERATURA'], 
                        label=estado, alpha=0.7)
            
            plt.title(f'Série Temporal de Temperatura por Estado - {regiao}')
            plt.xlabel('Data')
            plt.ylabel('Temperatura (°C)')
            plt.xticks(rotation=45)
            plt.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)
            
            salvar_grafico(plt, reports_dir, f'temp_temporal_estados_{regiao.lower()}.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar série temporal por estados para {regiao}: {str(e)}")

def plot_estatisticas_estados(dfs_dict, reports_dir):
    """Gera gráfico de estatísticas por estado"""
    try:
        configurar_estilo()
        fig, axes = plt.subplots(2, 1, figsize=(15, 12))
        
        dados_estados = []
        for regiao, df in dfs_dict.items():
            if 'ESTADO' in df.columns:
                for estado in df['ESTADO'].unique():
                    dados_estado = df[df['ESTADO'] == estado]
                    estatisticas = {
                        'Estado': estado,
                        'Região': regiao,
                        'Média': dados_estado['TEMPERATURA'].mean(),
                        'Mínima': dados_estado['TEMPERATURA'].min(),
                        'Máxima': dados_estado['TEMPERATURA'].max(),
                        'Amplitude': dados_estado['TEMPERATURA'].max() - dados_estado['TEMPERATURA'].min(),
                        'Desvio Padrão': dados_estado['TEMPERATURA'].std()
                    }
                    dados_estados.append(estatisticas)
        
        if dados_estados:
            df_stats = pd.DataFrame(dados_estados)
            
            # Gráfico de média, mínima e máxima
            df_stats.plot(x='Estado', y=['Média', 'Mínima', 'Máxima'], 
                         kind='bar', ax=axes[0], width=0.8)
            axes[0].set_title('Temperaturas Médias, Mínimas e Máximas por Estado')
            axes[0].set_xlabel('Estado')
            axes[0].set_ylabel('Temperatura (°C)')
            axes[0].tick_params(axis='x', rotation=45)
            axes[0].grid(True)
            
            # Gráfico de amplitude e desvio padrão
            df_stats.plot(x='Estado', y=['Amplitude', 'Desvio Padrão'],
                         kind='bar', ax=axes[1], width=0.8)
            axes[1].set_title('Amplitude Térmica e Desvio Padrão por Estado')
            axes[1].set_xlabel('Estado')
            axes[1].set_ylabel('Temperatura (°C)')
            axes[1].tick_params(axis='x', rotation=45)
            axes[1].grid(True)
            
            plt.tight_layout()
            salvar_grafico(plt, reports_dir, 'temp_estatisticas_estados.png')
        
    except Exception as e:
        logger.error(f"Erro ao gerar estatísticas por estado: {str(e)}")

def plot_radar_estado_capital(df, estado, reports_dir):
    """Gera gráfico de radar comparando métricas entre estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(10, 10))
            
            # Calcular métricas
            metricas = {
                'Média': df.groupby('TIPO')['TEMPERATURA'].mean(),
                'Máxima': df.groupby('TIPO')['TEMPERATURA'].max(),
                'Mínima': df.groupby('TIPO')['TEMPERATURA'].min(),
                'Amplitude': df.groupby('TIPO')['TEMPERATURA'].agg(lambda x: x.max() - x.min()),
                'Desvio': df.groupby('TIPO')['TEMPERATURA'].std()
            }
            
            # Preparar dados para o radar
            categorias = list(metricas.keys())
            valores_estado = [metricas[m]['ESTADO'] for m in categorias]
            valores_capital = [metricas[m]['CAPITAL'] for m in categorias]
            
            # Criar gráfico radar
            angulos = np.linspace(0, 2*np.pi, len(categorias), endpoint=False)
            angulos = np.concatenate((angulos, [angulos[0]]))  # Fechar o polígono
            
            valores_estado = np.concatenate((valores_estado, [valores_estado[0]]))
            valores_capital = np.concatenate((valores_capital, [valores_capital[0]]))
            
            ax = plt.subplot(111, projection='polar')
            ax.plot(angulos, valores_estado, 'o-', label='Estado')
            ax.plot(angulos, valores_capital, 'o-', label='Capital')
            ax.fill(angulos, valores_estado, alpha=0.25)
            ax.fill(angulos, valores_capital, alpha=0.25)
            
            ax.set_xticks(angulos[:-1])
            ax.set_xticklabels(categorias)
            plt.title(f'Comparação de Métricas - {estado}')
            plt.legend(bbox_to_anchor=(0.95, 0.95))
            
            salvar_grafico(plt, reports_dir, f'radar_estado_capital_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar radar para {estado}: {str(e)}")

def plot_violino_estado_capital(df, estado, reports_dir):
    """Gera gráfico de violino comparando distribuições entre estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(10, 6))
            
            sns.violinplot(data=df, x='TIPO', y='TEMPERATURA')
            plt.title(f'Distribuição de Temperatura - {estado}')
            plt.xlabel('Região')
            plt.ylabel('Temperatura (°C)')
            
            salvar_grafico(plt, reports_dir, f'violino_estado_capital_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar violino para {estado}: {str(e)}")

def plot_ciclo_diario_estado_capital(df, estado, reports_dir):
    """Gera gráfico de ciclo diário comparando estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(12, 6))
            
            for tipo in ['ESTADO', 'CAPITAL']:
                dados = df[df['TIPO'] == tipo]
                media_hora = dados.groupby('HORA')['TEMPERATURA'].mean()
                plt.plot(media_hora.index, media_hora.values, 'o-', label=tipo)
            
            plt.title(f'Ciclo Diário de Temperatura - {estado}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Temperatura Média (°C)')
            plt.grid(True)
            plt.legend()
            
            salvar_grafico(plt, reports_dir, f'ciclo_diario_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar ciclo diário para {estado}: {str(e)}")

def plot_calor_horario_estado_capital(df, estado, reports_dir):
    """Gera mapa de calor horário comparando estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            for tipo, ax in zip(['ESTADO', 'CAPITAL'], [ax1, ax2]):
                dados = df[df['TIPO'] == tipo]
                pivot = dados.pivot_table(
                    values='TEMPERATURA',
                    index='DIA_SEMANA',
                    columns='HORA',
                    aggfunc='mean'
                )
                
                sns.heatmap(pivot, ax=ax, cmap='RdYlBu_r', center=pivot.mean().mean())
                ax.set_title(f'Temperatura por Hora - {tipo}')
                
            plt.suptitle(f'Comparação de Padrões Horários - {estado}')
            plt.tight_layout()
            
            salvar_grafico(plt, reports_dir, f'calor_horario_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar mapa de calor horário para {estado}: {str(e)}")

def plot_densidade_estado_capital(df, estado, reports_dir):
    """Gera gráfico de densidade comparando estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(10, 6))
            
            for tipo in ['ESTADO', 'CAPITAL']:
                dados = df[df['TIPO'] == tipo]
                sns.kdeplot(data=dados, x='TEMPERATURA', label=tipo, fill=True)
            
            plt.title(f'Densidade de Temperatura - {estado}')
            plt.xlabel('Temperatura (°C)')
            plt.ylabel('Densidade')
            plt.legend()
            
            salvar_grafico(plt, reports_dir, f'densidade_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar densidade para {estado}: {str(e)}")

def plot_boxen_estado_capital(df, estado, reports_dir):
    """Gera boxenplot comparando estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(10, 6))
            
            sns.boxenplot(data=df, x='TIPO', y='TEMPERATURA')
            plt.title(f'Distribuição Detalhada de Temperatura - {estado}')
            plt.xlabel('Região')
            plt.ylabel('Temperatura (°C)')
            
            salvar_grafico(plt, reports_dir, f'boxen_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar boxenplot para {estado}: {str(e)}")

def plot_regressao_estado_capital(df, estado, reports_dir):
    """Gera gráfico de regressão comparando estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(10, 6))
            
            dados_estado = df[df['TIPO'] == 'ESTADO']['TEMPERATURA'].values
            dados_capital = df[df['TIPO'] == 'CAPITAL']['TEMPERATURA'].values
            
            plt.scatter(dados_estado, dados_capital, alpha=0.5)
            
            # Adicionar linha de regressão
            z = np.polyfit(dados_estado, dados_capital, 1)
            p = np.poly1d(z)
            plt.plot(dados_estado, p(dados_estado), "r--", alpha=0.8)
            
            plt.title(f'Correlação Estado-Capital - {estado}')
            plt.xlabel('Temperatura Estado (°C)')
            plt.ylabel('Temperatura Capital (°C)')
            
            # Adicionar linha de igualdade
            plt.plot([min(dados_estado), max(dados_estado)],
                    [min(dados_estado), max(dados_estado)],
                    'k--', alpha=0.3, label='Linha de Igualdade')
            
            plt.legend()
            
            salvar_grafico(plt, reports_dir, f'regressao_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar regressão para {estado}: {str(e)}")

def plot_barras_estado_capital(df, estado, reports_dir):
    """Gera gráfico de barras comparando métricas entre estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(12, 6))
            
            metricas = {
                'Média': df.groupby('TIPO')['TEMPERATURA'].mean(),
                'Mediana': df.groupby('TIPO')['TEMPERATURA'].median(),
                'Desvio': df.groupby('TIPO')['TEMPERATURA'].std(),
                'IQR': df.groupby('TIPO')['TEMPERATURA'].agg(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
            }
            
            dados_plot = pd.DataFrame(metricas)
            
            dados_plot.plot(kind='bar', width=0.8)
            plt.title(f'Métricas de Temperatura - {estado}')
            plt.xlabel('Região')
            plt.ylabel('Temperatura (°C)')
            plt.legend(title='Métrica')
            plt.grid(True, alpha=0.3)
            
            salvar_grafico(plt, reports_dir, f'barras_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar barras para {estado}: {str(e)}")

def plot_area_estado_capital(df, estado, reports_dir):
    """Gera gráfico de área comparando variação temporal entre estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            plt.figure(figsize=(12, 6))
            
            for tipo in ['ESTADO', 'CAPITAL']:
                dados = df[df['TIPO'] == tipo]
                plt.fill_between(dados['HORA'], 
                               dados.groupby('HORA')['TEMPERATURA'].mean() - dados.groupby('HORA')['TEMPERATURA'].std(),
                               dados.groupby('HORA')['TEMPERATURA'].mean() + dados.groupby('HORA')['TEMPERATURA'].std(),
                               alpha=0.3, label=f'{tipo} (±1 DP)')
                plt.plot(dados.groupby('HORA')['TEMPERATURA'].mean(), label=tipo)
            
            plt.title(f'Variação Diária com Incerteza - {estado}')
            plt.xlabel('Hora do Dia')
            plt.ylabel('Temperatura (°C)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            salvar_grafico(plt, reports_dir, f'area_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar área para {estado}: {str(e)}")

def plot_polar_estado_capital(df, estado, reports_dir):
    """Gera gráfico polar comparando padrões horários entre estado e capital"""
    try:
        if 'TIPO' in df.columns:
            configurar_estilo()
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), subplot_kw={'projection': 'polar'})
            
            for tipo, ax in zip(['ESTADO', 'CAPITAL'], [ax1, ax2]):
                dados = df[df['TIPO'] == tipo]
                medias = dados.groupby('HORA')['TEMPERATURA'].mean()
                
                # Converter horas para ângulos
                angulos = np.linspace(0, 2*np.pi, 24, endpoint=False)
                
                # Plotar dados
                ax.plot(angulos, medias.values)
                ax.fill(angulos, medias.values, alpha=0.25)
                ax.set_title(f'{tipo}')
                ax.set_xticks(angulos)
                ax.set_xticklabels([f'{h:02d}h' for h in range(24)], fontsize=8)
                
            plt.suptitle(f'Padrão Horário de Temperatura - {estado}')
            
            salvar_grafico(plt, reports_dir, f'polar_{estado.lower()}.png')
            
    except Exception as e:
        logger.error(f"Erro ao gerar polar para {estado}: {str(e)}")
