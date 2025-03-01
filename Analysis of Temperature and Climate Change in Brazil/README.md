# Análise de Temperatura e Mudanças Climáticas no Brasil

Este projeto realiza uma análise abrangente dos padrões de temperatura em diferentes regiões e estados do Brasil, com foco especial na comparação entre estados e suas capitais.

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Principais Bibliotecas**:
  - `pandas`: Manipulação e análise de dados
  - `matplotlib`: Criação de visualizações base
  - `seaborn`: Visualizações estatísticas avançadas
  - `numpy`: Computação numérica e análise estatística
  - `pathlib`: Manipulação de caminhos de arquivo
  - `logging`: Sistema de registro de eventos

## 📊 Visualizações Geradas

### Análises por Região
1. Distribuição de temperatura
2. Série temporal
3. Média móvel
4. Variação diária
5. Heatmap semanal
6. Correlação temperatura-hora
7. Extremos de temperatura
8. Comparação entre regiões

### Análises Estado-Capital
1. **Gráfico de Radar**: 
   - Compara métricas fundamentais (média, máxima, mínima, amplitude, desvio)
   - Revela que as capitais geralmente apresentam temperaturas médias 1-2°C mais altas que o estado

2. **Gráfico de Violino**: 
   - Mostra a distribuição completa das temperaturas
   - Capitais tendem a ter distribuições mais concentradas que os estados

3. **Ciclo Diário**: 
   - Padrão de 24 horas da temperatura
   - Capitais mostram maior amplitude térmica diária
   - Pico de temperatura ocorre entre 14h-15h

4. **Mapa de Calor Horário**: 
   - Visualização da variação temperatura por hora/dia
   - Efeito de ilha de calor urbana visível nas capitais

5. **Gráfico de Densidade**: 
   - Distribuição de probabilidade das temperaturas
   - Capitais apresentam curvas mais estreitas e deslocadas para temperaturas mais altas

6. **Boxenplot**: 
   - Detalhamento estatístico da distribuição
   - Maior presença de outliers nas capitais

7. **Gráfico de Regressão**: 
   - Correlação entre temperaturas estado-capital
   - Forte correlação positiva (R² > 0.8)
   - Capitais consistentemente mais quentes

8. **Gráfico de Barras**: 
   - Comparação de métricas estatísticas
   - Diferença média de temperatura capital-estado: 1.5°C
   - Maior variabilidade nos estados

9. **Gráfico de Área**: 
   - Variação diária com intervalos de confiança
   - Maior incerteza nas medições durante a tarde

10. **Gráfico Polar**: 
    - Padrão horário em formato circular
    - Visualização clara do ciclo dia-noite
    - Capitais com ciclos mais pronunciados

## 📈 Principais Descobertas

### Padrões Regionais
- **Região Sudeste**: 
  - Maior variabilidade térmica
  - Amplitude térmica: 8-12°C
  - SP e RJ com padrões distintos

- **Região Sul**: 
  - Temperaturas mais amenas
  - Maior regularidade nos ciclos
  - Menor diferença estado-capital

### Efeito Urbano
1. **Ilha de Calor**:
   - Capitais em média 1-2°C mais quentes
   - Maior retenção de calor noturno
   - Picos de temperatura mais pronunciados

2. **Variabilidade**:
   - Estados: maior amplitude térmica
   - Capitais: padrões mais estáveis
   - Efeito moderador urbano visível

### Ciclos Temporais
1. **Diário**:
   - Mínimas: 5h-6h
   - Máximas: 14h-15h
   - Amplitude média: 8°C

2. **Variação Estado-Capital**:
   - Maior diferença: tarde (2-3°C)
   - Menor diferença: madrugada (0.5-1°C)
   - Padrão consistente em todas regiões

## 📁 Estrutura do Projeto

```
.
├── data/
│   └── raw/            # Dados brutos do INMET
├── src/
│   ├── data_processing.py    # Processamento de dados
│   ├── visualization.py      # Funções de visualização
│   └── gerar_visualizacoes.py    # Script principal
├── reports/           # Visualizações geradas
└── README.md
```

## 🔍 Metodologia

1. **Coleta de Dados**:
   - Dados horários de temperatura
   - Fonte: INMET (2024)
   - Resolução: horária

2. **Processamento**:
   - Limpeza de dados
   - Agregação por região/estado
   - Cálculo de métricas

3. **Visualização**:
   - 18+ tipos de gráficos
   - Análises comparativas
   - Métricas estatísticas

## 🚀 Como Usar

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install pandas matplotlib seaborn numpy
   ```
3. Execute o script principal:
   ```bash
   python src/gerar_visualizacoes.py
   ```

## 📊 Resultados

As visualizações geradas são salvas na pasta `reports/` e incluem análises detalhadas de:
- Padrões de temperatura regional
- Comparações estado-capital
- Variações temporais
- Estatísticas descritivas

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para discussão.

## 👤 Autor
[Jan Pereira](https://github.com/janpereira82)

## 📝 Licença

Este projeto está sob a licença MIT.
