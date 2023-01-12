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
    },
    data() {
        return {}
    }
}
</script>
<style>

</style>
