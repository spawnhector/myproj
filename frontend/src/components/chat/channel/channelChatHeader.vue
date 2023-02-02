<template>
    <q-header elevated>
        <q-toolbar class="ChannelChatHeader">
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
        return { auth, channelChat, steps: null, skipStep: null }
    },
    computed: {
        headerLeft() {
            let _this = this;
            if (_this.channelChat.tutorial.currentStepIndex >= 2) {
                _this.skipStep.classList.remove("show")
                _this.skipStep.removeEventListener('click', _this.skipStepFunc);
            }
            const stepper = () => {
                return _this.channelChat.tutorial.active ? `
                        <div>
                            <ul class="stepper">
                                <li><span>Getting Started</span></li>
                                <li><span>Verify Account</span></li>
                                <li><span>Get Free Signal</span></li>
                            </ul>
                        </div>
                    ` : ``;
            }
            const userAccess = () => {
                return `<span>${'@' + _this.auth.user.username}${_this.currentChannel ? ` - ` + _this.currentChannel.channel : ``}</span>`;
            }
            const action = () => {
                return _this.channelChat.tutorial.active ?
                    `<span id="skipStep">Skip this step</span>` :
                    `<span id="linkAccount">Link Account</span>`;
            }
            return `
                ${_this.auth.isAuthenticated ?
                    `<div class="usersData">
                        <div class="useraccess">${userAccess()}</div>
                        <div class="action">${action()}</div>
                    </div>
                    ${stepper()}
                    `  : 'Guest'}
            `
        }
    },
    methods: {
        skipStepFunc() {
            this.channelChat.setState('tutorial', {
                ...this.channelChat.tutorial,
                currentStepIndex: this.channelChat.tutorial.currentStepIndex + 1,
            })
            this.steps[this.channelChat.tutorial.currentStepIndex].classList.add("is-active");
        }
    },
    mounted() {
        let _this = this;
        this.$nextTick(() => {
            _this.skipStep = document.getElementById('skipStep');
            _this.steps = document.querySelectorAll(".stepper li");
            if (typeof (_this.steps) != 'undefined' && _this.steps.length > 0) {
                var delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                delay(1000).then(() => {
                    _this.steps[_this.channelChat.tutorial.currentStepIndex].classList.add("is-active");
                });
            }
            if (typeof (_this.skipStep) != 'undefined' && _this.skipStep != null) {
                _this.skipStep.classList.add("show")
                _this.skipStep.addEventListener('click', _this.skipStepFunc)
            }
        })
    }
}
</script>
<style lang="scss">
.stepper {
    list-style: none;
    display: flex;
    flex-wrap: nowrap;
    padding: 10px 0px 0px 0px;

    >li {
        flex: 0 0 160px;
        position: relative;
        padding-bottom: 30px;

        span {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 11px;
            opacity: 0;
            transition: 0.75s opacity ease-in;
        }

        &:before {
            content: "";
            position: absolute;
            left: 50%;
            top: -5px;
            background: #24292e;
            box-sizing: border-box;
            width: 1em;
            z-index: 1;
            height: 1em;
            border: 2px solid white;
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
    color: #ffffff9c;

    .content {
        position: absolute;
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        align-content: center;
        justify-content: center;
        align-items: center;

        .usersData {
            position: relative;
            top: 0;

            .useraccess {}

            .action {
                font-size: 11px;
                text-decoration: underline;
                cursor: pointer;
                color: white;

                #skipStep {
                    display: none;

                    &.show {
                        display: block;
                    }
                }

                &:hover {
                    color: #757575;
                }
            }
        }
    }
}

.q-layout__section--marginal {
    background: rgba(255, 255, 255, 0.07) !important;
    color: #fff;
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
