<template>
    <div>
        <q-carousel ref="tutorial" v-model="step" transition-prev="jump-left" transition-next="jump-left" animated
            padding class="text-white">
            <q-carousel-slide name="stepOne" class="text-center">
                <q-scroll-area class="fit">
                    <StepOne />
                </q-scroll-area>
            </q-carousel-slide>
            <q-carousel-slide name="stepTwo" class="text-center">
                <q-scroll-area class="fit">
                    <StepTwo />
                </q-scroll-area>
            </q-carousel-slide>
            <q-carousel-slide name="stepThree" class="text-center">
                <q-scroll-area class="fit">
                    <StepThree />
                </q-scroll-area>
            </q-carousel-slide>
        </q-carousel>
    </div>
</template>

<script>
import { useQuasar } from 'quasar';

import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../../../lib/store.js';
import StepOne from './steps/step1.vue';
import StepTwo from './steps/step2.vue';
import StepThree from './steps/step3.vue';

export default {
    name: 'Tutorial',
    components: {
        StepOne, StepTwo, StepThree
    },
    props: [],
    computed: {
        height() {
            let _this = this
            return `${_this.$q.screen.height - 171}px`
        }
    },
    created() {
        let _this = this
        this.$watch('channelChat.tutorial.currentStepIndex', (val) => {
            _this.step = _this.getStep(val)
        })
    },
    methods: {
        getStep(index) {
            switch (index) {
                case 0:
                    return 'stepOne'
                    break;
                case 1:
                    return 'stepTwo'
                    break;
                case 2:
                    return 'stepThree'
                    break;
            }
        }
    },
    data() {
        let _this = this
        const channelChat = useChannelChat()
        return {
            channelChat,
            step: _this.getStep(channelChat.tutorial.currentStepIndex)
        }
    }
}
</script>
<style>

</style>
