<template></template>

<script>
import { useChannelChat } from '../../../lib/store.js';

export default {
    name: 'ChannelOnline',
    components: {
    },
    props: [],
    data() {
        const channelChat = useChannelChat()
        return { channelChat }
    }
}
</script>
<style></style>
