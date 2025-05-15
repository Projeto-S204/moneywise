document.addEventListener("DOMContentLoaded", function () {
  if (
    typeof receitasPorCategoria === "undefined" ||
    typeof despesasPorCategoria === "undefined"
  ) {
    console.error("Dados de categorias não encontrados");
    return;
  }

  const receitasLabels = receitasPorCategoria.map((item) => item[0]);
  const receitasValues = receitasPorCategoria.map((item) => item[1]);

  const despesasLabels = despesasPorCategoria.map((item) => item[0]);
  const despesasValues = despesasPorCategoria.map((item) => item[1]);

  Plotly.newPlot(
    "graficoReceitasCategoria",
    [
      {
        type: "pie",
        labels: receitasLabels,
        values: receitasValues,
        textinfo: "label+percent",
        hole: 0.4,
      },
    ],
    {
      title: "Receitas por Categoria",
    }
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
      },
    ],
    {
      title: "Despesas por Categoria",
    }
  );
});
