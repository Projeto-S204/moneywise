const layoutTemplate = {
  font: { color: "#E6E6E6", family: "Josefin Sans, sans-serif" },
  paper_bgcolor: "#1F1F23",
  plot_bgcolor: "#1F1F23",
  xaxis: {
    color: "#999999",
    gridcolor: "#323232",
    tickfont: { family: "Josefin Sans, sans-serif" },
  },
  yaxis: {
    color: "#999999",
    gridcolor: "#323232",
    tickfont: { family: "Josefin Sans, sans-serif" },
  },
  legend: {
    font: { color: "#E6E6E6", family: "Josefin Sans, sans-serif" },
    bgcolor: "#1F1F23",
    bordercolor: "#323232",
  },
  margin: { l: 40, r: 40, t: 60, b: 40 },
};

document.addEventListener("DOMContentLoaded", function () {
  // === 1. Gráfico de pizza - Receitas por categoria ===
  const receitasLabels = receitasPorCategoria.map((item) => item[0]);
  const receitasValues = receitasPorCategoria.map((item) =>
    parseFloat(item[1])
  );

  Plotly.newPlot(
    "graficoReceitasCategoria",
    [
      {
        type: "pie",
        labels: receitasLabels,
        values: receitasValues,
        textinfo: "label+percent",
        hole: 0.4,
        marker: {
          colors: ["#F2DF85", "#9F1631", "#F97E94", "#822C39"],
        },
      },
    ],
    {
      ...layoutTemplate,
      title: "Receitas por Categoria",
    }
  );

  // === 2. Gráfico de pizza - Despesas por categoria ===
  const despesasLabels = despesasPorCategoria.map((item) => item[0]);
  const despesasValues = despesasPorCategoria.map((item) =>
    parseFloat(item[1])
  );

  Plotly.newPlot(
    "graficoDespesasCategoria",
    [
      {
        type: "pie",
        labels: despesasLabels,
        values: despesasValues,
        textinfo: "label+percent",
        hole: 0.4,
        marker: {
          colors: ["#F2DF85", "#9F1631", "#F97E94", "#822C39"],
        },
      },
    ],
    {
      ...layoutTemplate,
      title: "Despesas por Categoria",
    }
  );

  // === 3. Gráfico de linha - Evolução do saldo ===
  const datas = saldoEvolucao.map((item) => item[0]);
  const saldos = saldoEvolucao.map((item) => parseFloat(item[1]));

  Plotly.newPlot(
    "graficoEvolucaoSaldo",
    [
      {
        x: datas,
        y: saldos,
        type: "scatter",
        mode: "lines+markers",
        line: { shape: "linear", color: "#004FFF" },
        marker: { color: "#004FFF" },
      },
    ],
    {
      ...layoutTemplate,
      title: "Evolução do Saldo",
      xaxis: { ...layoutTemplate.xaxis, title: "Data" },
      yaxis: { ...layoutTemplate.yaxis, title: "Saldo (R$)" },
    }
  );

  // === 4. Gráfico de barras - Comparativo receitas x despesas ===
  const meses = comparativoMensal.map((item) => item[0]);
  const receitasMes = comparativoMensal.map((item) => parseFloat(item[1]));
  const despesasMes = comparativoMensal.map((item) => parseFloat(item[2]));

  Plotly.newPlot(
    "graficoComparativo",
    [
      {
        x: meses,
        y: receitasMes,
        name: "Receitas",
        type: "bar",
        marker: { color: "#F2DF85" },
      },
      {
        x: meses,
        y: despesasMes,
        name: "Despesas",
        type: "bar",
        marker: { color: "#9F1631" },
      },
    ],
    {
      ...layoutTemplate,
      barmode: "group",
      title: "Comparativo: Receitas x Despesas",
      xaxis: { ...layoutTemplate.xaxis, title: "Mês" },
      yaxis: { ...layoutTemplate.yaxis, title: "Valor (R$)" },
    }
  );

  // === 5. Gráfico de barra horizontal - Top 5 maiores despesas ===
  const top5Labels = top5Despesas.map((item) => item[0]);
  const top5Valores = top5Despesas.map((item) => parseFloat(item[1]));

  Plotly.newPlot(
    "graficoTop5Despesas",
    [
      {
        y: top5Labels,
        x: top5Valores,
        type: "bar",
        orientation: "h",
        marker: { color: "#004FFF" },
      },
    ],
    {
      ...layoutTemplate,
      title: "Top 5 Maiores Despesas",
      xaxis: { ...layoutTemplate.xaxis, title: "Valor (R$)" },
    }
  );
});
