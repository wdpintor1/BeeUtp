var nombreGrupo = 'sensores';
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chart/'
    +nombreGrupo
    +'/'
);

chatSocket.onmessage = function(e) {         
    var data = JSON.parse(e.data);
    var valor=document.querySelector('#chat-message-input').value;
    valor = (data.message + '\n');
    //Agregamos codigo para ciclado de los charts
    var items = document.querySelectorAll('.item');   
    var myChart;

items.forEach(function(item) {
    var canvasId = 'myLineChart' + item.dataset.itemId;
    var canvas = document.getElementById(canvasId);
    if (canvas) {    
        // Continúa con las operaciones del gráfico
        myChart.data.labels.push(new Date().toLocaleTimeString());
        myChart.data.datasets[0].data.push(data.message);
        myChart.update();
    } else {
        console.error('Elemento canvas no encontrado:', canvasId);
    }
    });
    
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};