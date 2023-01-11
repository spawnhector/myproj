<template>
    <div>
        <q-icon name="trending_up" class="text-green" />{{ signal }}<span class="text-green f-10">20<q-icon
                name="percent" /></span>
    </div>
</template>

<script>
export default {
    name: 'SignalList',
    components: {
    },
    props: ['signal'],
    beforeMount() {
        const socket = new WebSocket('ws://localhost:8080');
        socket.onopen = function (event) {
            console.log('WebSocket is open now.');
            // you can send message to the server once the connection is open
            socket.send('Hello Server!');
        };
        socket.onmessage = function (event) {
            console.log('Received: ' + event.data);
        };

        socket.onclose = function (event) {
            console.log('WebSocket is closed now.');
        };
        socket.onerror = function (error) {
            console.error(`WebSocket error: ${error}`);
        };
    },
    data() {
        return {}
    }
}
</script>
<style>

</style>
