# Dashboard Barbearia

**Disciplina:** Sistemas de Apoio à Decisão (SAD)  
**Atividade:** Visualização e análise de dados de atendimentos de uma barbearia  

---

## Descrição

Este projeto é um **dashboard interativo** desenvolvido em **Python** utilizando **Streamlit** e **Plotly**, com o objetivo de analisar os atendimentos diários de uma barbearia ao longo de um ano.  

O dashboard permite visualizar os atendimentos:  

- Por dia  
- Por semana  
- Por mês  

As métricas principais exibidas são:  

- Total de atendimentos  
- Média diária de atendimentos  
- Média semanal de atendimentos  
- Dia mais movimentado  
- Dia da semana mais movimentado  

O dataset é simulado com base em padrões realistas de atendimento, incluindo sazonalidade:  

- Janeiro/Fevereiro: movimento menor (férias)  
- Março a Junho: normal  
- Julho e Dezembro: aumento de atendimentos (férias e festas)  
- Domingos: barbearia fechada  

---

## Tecnologias Utilizadas

- Python 3.x  
- [Streamlit](https://streamlit.io/)  
- [Plotly](https://plotly.com/python/)  
- [Pandas](https://pandas.pydata.org/)  
- [NumPy](https://numpy.org/)  

---

## Instalação

1. **Clonar o repositório ou baixar os arquivos**  

2. **Instalar as dependências**  
   ```bash
   python -m pip install streamlit plotly pandas numpy

3. **Executar o script**
  ```bash
  python -m streamlit run dashboard.py

