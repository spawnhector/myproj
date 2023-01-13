<template>
    <div>
        <q-icon name="trending_up" class="text-green" />{{ signal }}<span class="text-green f-10">{{ percent }}<q-icon
                name="percent" /></span>
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
    }
}
</script>
<style>

</style>
