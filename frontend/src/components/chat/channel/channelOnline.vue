<template>
    <div class="signal_channel_status">
        <q-badge :color="color" rounded class="q-mr-sm" />{{ onlineText }}
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
            return this.channelOnline ? "Online" : "Offline";
        }
    }
}
</script>
<style lang="scss">
.signal_channel_status {
    position: absolute;
    right: 61px;
}
</style>
