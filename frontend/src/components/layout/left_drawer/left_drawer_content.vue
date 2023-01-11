<template>
    <div id="vue-list-animation-test" class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-12 left_drawer_container">
                <ul class="list-group">
                    <div class="bg-dark-container text-white">
                        <q-list dark>
                            <q-expansion-item v-for="(signals, pair) in items" v-bind:key="pair" :label="pair">
                                <q-card class="bg-grey-9">
                                    <q-card-section>
                                        <transition-group name="list-complete" tag="li">
                                            <li v-for="signal in signals" v-bind:key="signal[2]"
                                                class="list-group-item list-complete-item">
                                                <signal-list :signal="signal[2]" />
                                            </li>
                                        </transition-group>
                                    </q-card-section>
                                </q-card>
                            </q-expansion-item>
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
        nextNum: 6
    }),
    beforeMount() {
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
        getSignals: function () {
            let _this = this;
            GetSignals().then(res => {
                _this.items = _this.groupArray(res.data.pairs, 1);
            }, err => {
                console.log('signal err', err)
            })
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
