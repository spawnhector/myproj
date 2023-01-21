<template>
    <q-page>
        <chat />
    </q-page>
</template>

<script>
import chat from '../../components/chat/chat.vue';

export default {
    name: 'Home',
    components: {
        chat
    },
    data: () => ({
    }),
}
</script>
<style lang="sass">
.sub_layer_container
    background: #1A1A2A
</style>
