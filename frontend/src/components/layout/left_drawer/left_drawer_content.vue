<template>
    <q-scroll-area class="fit side-container">
        <div id="vue-list-animation-test" class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-12 left_drawer_container">
                    <ul class="currency-card list-group">
                        <li class="list" v-show="showSimulatedReturnData" v-for="(signals, pair) in items"
                            v-bind:key="pair">
                            <q-list dark>
                                <q-expansion-item expand-separator>
                                    <template v-slot:header>
                                        <ListHeader :pair="pair" :signals="signals" />
                                    </template>
                                    <q-card class="bg-grey-9">
                                        <q-card-section class="signal-card">
                                            <transition-group name="list-complete" tag="li">
                        <li v-for="signal in signals" v-bind:key="signal[2]" class="list-group-item list-complete-item">
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
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </q-scroll-area>
</template>

<script>
import { GetSignals } from '../../../utils/apiRequest';
import ListHeader from './listheader.vue';
import signalList from './listSignal.vue';

export default {
    name: 'LeftDrawerContent',
    components: {
        signalList, ListHeader
    },
    data: () => ({
        items: {},
        nextNum: 6,
        visible: false,
        showSimulatedReturnData: false,
        socket: null,
        requests: 0,
        limit: 1000, // number of requests per minute
        interval: 60000, // interval in milliseconds
        lastCheck: Date.now(),
    }),
    computed: {
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
        shuffle: function (newVal) {
            let sortedObj = {};
            let sortedObj1 = {};
            let entries = Object.entries(newVal);
            // sort sub-array in object
            entries.forEach(([key, value]) => {
                sortedObj[key] = value.sort((a, b) => a[2] > b[2] ? 1 : -1);
            });
            entries = Object.entries(sortedObj);
            this.items = Object.fromEntries(entries.sort((a, b) => {
                let sumA = a[1].reduce((acc, current) => acc + current[3], 0);
                let sumB = b[1].reduce((acc, current) => acc + current[3], 0);
                return sumB - sumA;
            }));
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
        socketAction() {
            // if (this.requests >= this.limit) {
            //     this.socket.close()
            //     return;
            // }
            // if (Date.now() - this.lastCheck > this.interval) {
            //     this.lastCheck = Date.now();
            //     this.requests = 0;
            // }
            this.socket.send(`testing counter`);
            // this.requests++;
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
        createWebSocket() {
            let _this = this;
            _this.socket = new WebSocket('ws://localhost:8080');
            _this.socket.onopen = function (event) {
                _this.socketAction();
            };
            _this.socket.onmessage = function (event) {
                let data = JSON.parse(event.data)
                _this.items = _this.groupArray(data.pairs, 1);
                _this.visible = false;
                _this.showSimulatedReturnData = true;
                _this.items = _this.addPercentage(_this.items, data.currencyData);
                _this.shuffle(_this.items)
                // console.log(_this.items)
                _this.socketAction();
            };
            _this.socket.onclose = function (event) {
                _this.createWebSocket()
            };
            _this.socket.onerror = function (error) {
                console.error(`WebSocket error: ${error}`);
            };
        },
        getSignals: function () {
            // this.createWebSocket()
        }
    },
    mounted() {
        this.visible = true
        this.showSimulatedReturnData = false
        this.getSignals()
    },
}
</script>
<style lang="sass">
.left_drawer_container
    ul.currency-card
        list-style-type: none
        margin: 0px
        padding: 0px
        .list:first-child
            .q-item
                border-top-left-radius: 14px
                border-top-right-radius: 14px
        .list:last-child
            .q-item
                border-bottom-left-radius: 14px
                border-bottom-right-radius: 14px
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
            border-bottom: 1px solid white
            background-color: #1A1A2A
            padding-left: 10px
        .q-card__section--vert
            padding: 0px
            .text-green
                color: green
        .signal-card
            max-height: 200px
            overflow-y: scroll
            background-color: #1A1A2A
        .q-item
            background-color: rgba(255, 255, 255, 0.07)
</style>
