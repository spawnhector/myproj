<template>
    <div>
        <div class="row">
            <div class="col-2"> <q-icon :name="signalTrend" :class="signalColor" /> </div>
            <div class="col-6"> <span>{{ signal }}</span> </div>
            <div class="col-4"> <span :class="signalColor" class="f-10 list-percentage">{{ signalPercentage }}<q-icon
                        name="percent" /></span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SignalList',
    components: {
    },
    props: ['signal', 'percent'],
    beforeMount() {
    },
    data() {
        return {}
    },
    computed: {
        signalPercentage() {
            if (this.percent) return this.percent.toFixed(3);
            else return 0.000;
        },
        signalColor() {
            if (this.percent <= -0) {
                return "text-red";
            } else {
                return "text-green";
            }
        },
        signalTrend() {
            if (this.percent <= -0) {
                return "trending_down";
            } else {
                return "trending_up";
            }
        }
    }
}
</script>
<style>
.list-percentage {
    float: right;
    margin-right: 10px;
}
</style>
