<template>
    <div class="channel_body" :style="style">
        <Tutorial />
    </div>
</template>

<script>
import { useQuasar } from 'quasar';

import Tutorial from './tutorial/tutorial.vue';

export default {
    name: 'ChannelBody',
    components: {
        Tutorial
    },
    props: [],
    computed: {
        style() {
            let _this = this
            return `height: ${_this.$q.screen.height - 171}px`
        }
    },
    data() {
        const $q = useQuasar();
        return { $q }
    }
    , mounted() {
        console.log(this.$q.screen.height)
    }
}
</script>
<style lang="scss">
.channel_body {
    margin-top: 58px;
}
</style>
