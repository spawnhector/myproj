<template>
    <q-item-section avatar>
        <q-icon :class="color" :name="trend" />
    </q-item-section>
    <q-item-section> {{ pair }} </q-item-section>
    <q-item-section side>
        <div class="row items-center">
            <span :class="color" class="f-10 list-percentage">{{ percentageSum }}<q-icon name="percent" /></span>
        </div>
    </q-item-section>
</template>

<script>
export default {
    name: 'ListHeader',
    components: {
    },
    props: ['pair', 'signals'],
    data() {
        return {
            trend: '',
            color: ''
        }
    },
    computed: {
        percentageSum() {
            let sum = 0;
            for (let i = 0; i < this.signals.length; i++) {
                sum += this.signals[i][3];
            }
            sum = sum.toFixed(3);

            if (sum <= -0) {
                this.trend = 'trending_down';
                this.color = "text-red";
            } else {
                this.trend = 'trending_up';
                this.color = "text-green";
            }
            return sum;
        }
    }
}
</script>
<style>

</style>
