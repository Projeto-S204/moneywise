const ctx = document.getElementById('donutChart').getContext('2d');

const donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Entretenimento', 'Casa', 'Salário', 'Itens', 'Outros'],
        datasets: [{
            data: [20, 20, 20, 20, 20], // percentuais ou valores reais
            backgroundColor: [
                'var(--graph-color-1)',
                'var(--graph-color-2)',
                'var(--graph-color-3)',
                'var(--graph-color-4)',
                'var(--graph-color-5)'
            ],
            borderWidth: 0
        }]
    },
    options: {
        cutout: '50%', // cria o efeito donut
        plugins: {
            legend: {
                display: true,
                position: 'right',
                labels: {
                    color: 'black',
                    font: {
                        family: 'Josefin Sans',
                        size: 14
                    }
                }
            }
        }
    }
});

// Versao automatica do gráfico com fetch do backend 
// Recebe label e valor para que seja criado o grafico
const grf = document.getElementById('idGrafico').getContext('2d');

fetch('/dados')  // busca backend
.then(res => res.json())
.then(data => {
  new Chart(grf, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Receitas',
        data: data.valores,
        backgroundColor: '#4caf50'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
});
