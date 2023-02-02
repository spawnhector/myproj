<template>
    <div class="step-blur" :style="style">
    </div>
</template>

<script>
import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../../lib/store.js';

export default {
    name: 'Blur',
    components: {
    },
    computed: {
        style() {
            let _this = this;
            let bType = _this.$props.blurtype;
            return _this.activateBlur ? _this.channelChat.tutorial.blur.style[bType] : {
                display: 'none'
            }
        }
    },
    props: ['blurtype'],
    created() {
        let _this = this;
        this.$watch('channelChat.tutorial.currentStepIndex', val => {
            if (val == 2) _this.activateBlur = true;
        })
    },
    data() {
        let _this = this;
        const channelChat = useChannelChat()
        return { channelChat, activateBlur: channelChat.tutorial.currentStepIndex == 2 ? true : false }
    }
}
</script>
<style>

</style>
