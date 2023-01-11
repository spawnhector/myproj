<template>
    <q-tooltip transition-show="flip-right" transition-hide="flip-left" :target="targetEl"
        :class="{ 'bg-red': field != '' }" v-model="istoggled" anchor="center left" self="center right">{{
    text
        }}</q-tooltip>
</template>

<script>
export default {
    name: 'InputToolTip',
    props: ['togglestate', 'toggletext', 'field'],
    data() {
        let istoggled = this.togglestate;
        let text = this.toggletext;
        let targetEl = true;
        return {
            istoggled,
            text,
            targetEl
        }
    },
    created() {
        let _this = this
        this.$watch('togglestate', (newVal) => {
            _this.istoggled = newVal;
            _this.targetEl = newVal;
        })
        this.$watch('toggletext', (newVal) => {
            _this.text = newVal;
        })
    },
}
</script>
<style>

</style>
