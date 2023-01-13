<template>
    <div id="vue-list-animation-test" class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-12 left_drawer_container">
                <ul class="list-group">
                    <div class="bg-dark-container text-white">
                        <q-list dark>
                            <q-expansion-item v-show="showSimulatedReturnData" v-for="(signals, pair) in items"
                                v-bind:key="pair" :label="pair">
                                <q-card class="bg-grey-9">
                                    <q-card-section>
                                        <transition-group name="list-complete" tag="li">
                                            <li v-for="signal in signals" v-bind:key="signal[2]"
                                                class="list-group-item list-complete-item">
                                                <signal-list :signal="signal[2]" :percent="signal[3]" />
                                            </li>
                                        </transition-group>
                                    </q-card-section>
                                </q-card>
                            </q-expansion-item>
                            <q-inner-loading :showing="visible">
                                <q-spinner-gears size="50px" color="primary" />
                            </q-inner-loading>
                        </q-list>
                    </div>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import { GetSignals } from '../../../utils/apiRequest';
import signalList from './listSignal.vue';

export default {
    name: 'LeftDrawerContent',
    components: {
        signalList
    },
    data: () => ({
        items: [],
        nextNum: 6,
        testCounter: 0,
        visible: false,
        showSimulatedReturnData: false
    }),
    beforeMount() {
        this.visible = true
        this.showSimulatedReturnData = false
        this.getSignals()
    },
    methods: {
        randomIndex() {
            return Math.floor(Math.random() * this.items.length)
        },
        add() {
            this.items.splice(this.randomIndex(), 0, this.nextNum++)
        },
        remove() {
            this.items.splice(this.randomIndex(), 1)
        },
        arrShuffle(array) {
            let currentIndex = array.length, randomIndex;
            while (currentIndex != 0) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;
                [array[currentIndex], array[randomIndex]] = [
                    array[randomIndex], array[currentIndex]];
            }
            return array;
        },
        shuffle: function () {
            this.items = this.arrShuffle(this.items);
        },
        label() {
            // return <q-icon name='trending_up' class='text-green' />
        },
        groupArray(array, index) {
            const result = array.reduce((acc, curr) => {
                const key = curr[index];
                if (!acc[key]) {
                    acc[key] = [];
                }
                acc[key].push(curr);
                return acc;
            }, {});
            return result;
        },
        socketAction(socket) {
            // you can send message to the server once the connection is open
            socket.send(`testing counter ${this.testCounter}`);
            this.testCounter++
        },
        calculatePercentage(obj, arr) {
            for (const key in obj) {
                if (key === arr[1]) {
                    var initial = obj[key];
                }
            }
            var diff = initial - arr[2];
            var percent = (diff / initial) * 100;
            return percent;
        },
        addPercentage(obj, obj2) {
            let _this = this;
            for (const key in obj) {
                obj[key].forEach(subArr => {
                    subArr.push(_this.calculatePercentage(obj2, subArr));
                });
            }
            return obj;
        },
        getSignals: function () {
            let _this = this;
            const socket = new WebSocket('ws://localhost:8080');
            socket.onopen = function (event) {
                console.log('WebSocket is open now.');
                _this.socketAction(socket);
            };
            socket.onmessage = function (event) {
                let data = JSON.parse(event.data)
                _this.items = _this.groupArray(data.pairs, 1);
                _this.visible = false;
                _this.showSimulatedReturnData = true;
                console.log(_this.addPercentage(_this.groupArray(data.pairs, 1), data.currencyData));
                // _this.socketAction(socket);
            };
            socket.onclose = function (event) {
                console.log('WebSocket is closed now.');
            };
            socket.onerror = function (error) {
                console.error(`WebSocket error: ${error}`);
            };
            // let _this = this;
            // GetSignals().then(res => {
            //     _this.items = _this.groupArray(res.data.pairs, 1);
            // }, err => {
            //     console.log('signal err', err)
            // })
        }
    }
}
</script>
<style lang="sass">
.left_drawer_container
    ul.list-group
        list-style-type: none
        margin: 0px
        padding: 0px
        .list-complete-item
            transition: all .6s
        .list-complete-enter,
        .list-complete-leave-to
            opacity: 0
            transform: translateY(35px)
        .list-complete-leave-active
            position: relative
            display: block
        .list-group-item
            margin-bottom: 1px
            background-color: #1A1A2A
            padding-left: 10px
        .q-card__section--vert
            padding: 0px
            .text-green
                color: green

</style>
