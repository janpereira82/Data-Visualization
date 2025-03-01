# Food-101 Nutritional Analysis Dashboard

## 📊 Sobre o Projeto
Este dashboard interativo foi desenvolvido para análise nutricional do dataset Food-101, focando em auxiliar nutricionistas e pacientes na escolha de alimentos com base em seus valores nutricionais e combinações saudáveis.

## 👨‍💻 Autor
[Jan Pereira](https://github.com/janpereira82)

## 🎯 Principais Funcionalidades

### 1. Filtros Nutricionais
- **Nível de Recomendação**: Filtre por categorias de recomendação (Excelente, Bom, etc.)
- **Limite de Calorias**: Defina um limite máximo de calorias
- **Perfil Nutricional**: Selecione tipos específicos de alimentos
- **Nutrientes**: Configure valores mínimos para proteína e fibra, e máximos para açúcar e sódio

### 2. Análise de Alimentos
- **Score Nutricional**: Sistema de pontuação (0-100) baseado em:
  - Densidade de proteína (35%)
  - Densidade de fibra (35%)
  - Controle de açúcar (15%)
  - Controle de sódio (15%)

### 3. Perfis Nutricionais
- **Rico em Proteína**: >15g proteína por 100kcal
- **Alto em Fibra**: >7g fibra por 100kcal
- **Rico em Fibra**: ≥6g fibra (baseado em RDA)
- **Rico em Carboidratos Complexos**: >50% calorias de carboidratos e ≥4g fibra
- **Baixo Açúcar**: <5g açúcar
- **Balanceado**: Bom equilíbrio geral de nutrientes

### 4. Análise de Combinações
- Interface para seleção e análise de pares de alimentos
- Cálculo de métricas combinadas:
  - Calorias totais
  - Proteína total
  - Fibra total
  - Score nutricional médio
- Avaliação automática da combinação baseada nos critérios definidos

## 🚀 Como Usar

1. **Instalação**
```bash
pip install -r requirements.txt
```

2. **Executar o Dashboard**
```bash
streamlit run dashboard/app.py
```

3. **Navegação**
   - Use os filtros na barra lateral para refinar sua busca
   - Explore as melhores opções por perfil nutricional
   - Analise combinações personalizadas de alimentos
   - Consulte o detalhamento nutricional completo na tabela

## 📈 Métricas e Cálculos

### Score Nutricional
- **Proteína**: 35% do score final
  - Baseado na densidade (g/100kcal)
  - Meta: 20g/100kcal = 100 pontos

- **Fibra**: 35% do score final
  - Baseado na densidade (g/100kcal)
  - Meta: 10g/100kcal = 100 pontos

- **Açúcar**: 15% do score final
  - Pontuação inversa
  - Limite: 25g = 0 pontos

- **Sódio**: 15% do score final
  - Pontuação inversa
  - Limite: 2300mg = 0 pontos

### Níveis de Recomendação
- **Excelente**: Score > 75
- **Bom**: Score 50-75
- **Consumo Moderado**: Score 25-50
- **Evitar**: Score < 25

## 📚 Dataset
O dataset Food-101 foi enriquecido com informações nutricionais detalhadas para cada alimento, incluindo:
- Calorias
- Proteínas
- Carboidratos
- Gorduras
- Fibras
- Açúcares
- Sódio

## 🛠️ Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- Plotly Express
- NumPy

## 🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## 📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor
[Jan Pereira](https://github.com/janpereira82)
