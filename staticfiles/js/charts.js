document.addEventListener('DOMContentLoaded', function() {   
    var myCharts = {};
    // Suponiendo que 'charts' es un array de objetos
    for (let i = 0; i < chartsData.length; i++) {
        const chart = chartsData[i];
        var valorId=chart.id
        var canvasId='myLineChart' + valorId;
        var ctx = document.getElementById(canvasId).getContext('2d');
        var chartContainer = document.getElementById('chartContainer' + valorId);
        ctx.canvas.width = chartContainer.clientWidth;
        ctx.canvas.height = chartContainer.clientHeight;

        var initialChartData = {
            labels: chart.fechas,  // Etiquetas de tiempo iniciales
            datasets: [{
                label: chart.tituloGrafica,
                data: chart.medidas,  // Datos iniciales
                fill: true,
                borderColor: chart.color,
                backgroundColor:chart.color,
                tension: 0.1
            }]
        };
        // Configuración de opciones del gráfico
        var chartOptions = {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: chart.ejeY
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: chart.ejeX
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            // Otras opciones según tus necesidades
        };
        myCharts[valorId] = new Chart(ctx, {
            type: chart.tipo,
            data: initialChartData,
            options: chartOptions
        });
    }   
    /* Lineas para el web socket */
    var nombreGrupo=idCanal;
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chart/'
        +nombreGrupo
        +'/'
    );
    chatSocket.onmessage = function(e) {     
        var data = JSON.parse(e.data);
        valor = (data.message + '\n');
        // Ciclado de los charts
        for (var currentItem of data.message) {
            // Ahora puedes acceder a las propiedades de currentItem, por ejemplo, currentItem.medida
            var canvasId = 'myLineChart' + currentItem.id;
            var canvas = document.getElementById(canvasId);
            if (canvas) {
                myCharts[currentItem.id].data.labels.push(new Date().toLocaleTimeString());
                myCharts[currentItem.id].data.datasets[0].data.push(currentItem.medida);
                myCharts[currentItem.id].update();
            } else {
                console.error('Elemento canvas no encontrado:', canvasId);
            }
        }  
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});