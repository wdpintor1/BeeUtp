

// Configura las opciones del gráfico
var options = {
    scales: {
        y: {
            beginAtZero: true
        }
    }
};
document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los elementos con la clase "item"
    var items = document.querySelectorAll('.item');   
    // Iterar sobre los elementos y acceder a los datos
    items.forEach(function(item) {
        var valorId=item.dataset.itemId;
        var canvasId='myLineChart' + valorId;
        var ctx = document.getElementById(canvasId).getContext('2d');
        var chartContainer = document.getElementById('chartContainer'+item.dataset.itemId);
        ctx.canvas.width = chartContainer.clientWidth;
        ctx.canvas.height = chartContainer.clientHeight;
    });
});
