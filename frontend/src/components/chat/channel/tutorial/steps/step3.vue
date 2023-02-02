<template>
    <div class="instruction-container">
        <div class="instruction">
            <div class="sub-head">New User Give Away</div>
            <div>We are giving away one free channel to every new user who registered and verify there account before
                September 20,2030.</div>
            <div>
                <button type="button" class="submit" @click="activateChannelList()">Give Me Access</button>
            </div>
        </div>
        <div class="back-drop"></div>
    </div>
</template>

<script>
import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../../../../lib/store.js';

export default {
    name: 'StepThree',
    components: {
    },
    props: [],
    data() {
        const channelChat = useChannelChat();
        return { channelChat }
    },
    methods: {
        activateChannelList() {
            this.channelChat.setState('tutorial', {
                ...this.channelChat.tutorial,
                dsFreeChannel: true
            })
        }
    }
}
</script>
<style>

</style>
