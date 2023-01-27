<template>
    <q-header elevated>
        <q-toolbar class="bg-grey-3 text-black ChannelChatHeader">
            <div class="q-subtitle-1 content" v-html="headerLeft"></div>
            <q-space />
            <q-btn round flat icon="more_vert">
                <q-menu auto-close :offset="[110, 0]">
                    <q-list style="min-width: 150px">
                        <q-item clickable>
                            <q-item-section>Contact data</q-item-section>
                        </q-item>
                        <q-item clickable>
                            <q-item-section>Block</q-item-section>
                        </q-item>
                        <q-item clickable>
                            <q-item-section>Select messages</q-item-section>
                        </q-item>
                        <q-item clickable>
                            <q-item-section>Silence</q-item-section>
                        </q-item>
                        <q-item clickable>
                            <q-item-section>Clear messages</q-item-section>
                        </q-item>
                        <q-item clickable>
                            <q-item-section>Erase messages</q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
        </q-toolbar>
    </q-header>
</template>

<script>
import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../../lib/store.js';

export default {
    name: 'ChannelChatHeader',
    components: {
    },
    props: ['currentChannel'],
    data() {
        const auth = useAuthStore()
        const channelChat = useChannelChat()
        return { auth, channelChat, steps: null }
    },
    computed: {
        headerLeft() {
            return `
                ${this.auth.isAuthenticated ?
                    `<div class="usersData">
                        <div>${'@' + this.auth.user.username}</div>
                        <div class="action" id="skipStep">Skip this step</div>
                    </div>` +
                    (this.currentChannel ? this.currentChannel.channel :
                        `
                        <ul class="stepper">
                            <li><span>Getting Started</span></li>
                            <li><span>About Us</span></li>
                            <li><span>Cloud computing explored</span></li>
                        </ul>
                    `
                    ) : 'Guest'}
            `
        }
    },
    methods: {
        skipStep() {
            this.channelChat.setState('tutorial', {
                currentStepIndex: this.channelChat.tutorial.currentStepIndex + 1,
            })
            this.steps[this.channelChat.tutorial.currentStepIndex].classList.add("is-active");
        }
    },
    mounted() {
        let _this = this;
        this.$nextTick(() => {
            var skipStep = document.getElementById('skipStep')
            skipStep.addEventListener('click', _this.skipStep)
            _this.steps = document.querySelectorAll(".stepper li");
            var delay = ms => new Promise(resolve => setTimeout(resolve, ms));
            delay(1000).then(() => {
                _this.steps[_this.channelChat.tutorial.currentStepIndex].classList.add("is-active");
            });
        })
    }
}
</script>
<style lang="scss">
.stepper {
    list-style: none;
    display: flex;
    flex-wrap: nowrap;
    padding: 0px 0px 0px 78px;
    // top: -18px;
    // // left: -125px;
    // position: relative;

    >li {
        flex: 0 0 137px;
        position: relative;
        padding-bottom: 30px;

        span {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            opacity: 0;
            transition: 0.75s opacity ease-in;
        }

        &:before {
            content: "";
            position: absolute;
            left: 50%;
            top: -5px;
            background: white;
            box-sizing: border-box;
            width: 1em;
            z-index: 1;
            height: 1em;
            border: 2px solid #2109a7;
            border-radius: 50%;
            transform: translateX(-50%) scale(0);
            transition: 0.75s all ease-in;
        }

        &:not(:first-child):after {
            content: "";
            position: absolute;
            left: -50%;
            width: 0%;
            height: 5px;
            background: #00000063;
        }

        &.is-active span {
            opacity: 1;
        }

        &.is-active:before {
            transform: translateX(-50%) scale(1);
        }

        &.is-active:after {
            animation: stepper 0.5s ease-out forwards;
        }
    }
}

.ChannelChatHeader {
    .content {
        position: relative;

        .usersData {
            position: absolute;
            top: 10px;

            .action {
                font-size: 11px;
                text-decoration: underline;
                cursor: pointer;
                color: #0000ff94;

                &:hover {
                    color: blue;
                }
            }
        }
    }
}

@keyframes stepper {
    from {
        width: 0;
    }

    to {
        width: 100%;
    }
}
</style>
