<template>
    <div class="signal_channel_status">
        <q-badge :color="color" rounded class="q-mr-sm" />Signals are {{ onlineText }}
    </div>
</template>

<script>
import {
    mapActions,
    mapState,
} from 'pinia';

import { useChannelChat } from '../../../lib/store.js';

export default {
    name: 'ChannelOnline',
    components: {
    },
    props: [],
    data() {
        return {}
    },
    computed: {
        ...mapState(useChannelChat, [
            'channelOnline',
        ]),
        color() {
            return this.channelOnline ? "green" : "red";
        },
        onlineText() {
            return this.channelOnline ? "online" : "offline";
        }
    },
    created() {
        let _this = this;
        this.createChannelSocket()
        this.$watch('channelOnline', (online) => {
            if (!online) _this.reCreateChannelSocket();
        })
    },
    methods: {
        ...mapActions(useChannelChat, [
            'createChannelSocket',
            'reCreateChannelSocket',
            'setState'
        ]),
    }
}
</script>
<style lang="scss">
// .signal_channel_status {
//     // position: absolute;
//     // right: 61px;
// }
</style>
