<template>
    <div>
        <q-scroll-area :thumb-style="thumbStyle" :bar-style="barStyle" :style="style" ref="channelChatBody">
            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <div v-show="showChatData" class="channel-chat-body" v-scroll="handleScroll">
                    <div v-for="(chats, mainKey) in conversations"
                        :key="`${chats[0].trade_ticket}-conversation-start-${mainKey}`" class="item">
                        <div class="conversation-start">
                            <span>
                                <div :class="[newSignals[mainKey] ? 'new' : '']" :ref="`${mainKey}`" :name="mainKey">
                                    <q-chip size="sm" v-show="newSignals[mainKey]" square color="deep-orange"
                                        text-color="white"> New Signal </q-chip>
                                </div> {{ dateToHuman(mainKey) }}
                            </span>
                            <!-- <ConversationStart :mainKey="mainKey" /> -->
                        </div>
                        <div v-for="(chat, subKey) in chats" :key="`${chat.id}-chat-${subKey}`" class="bubble"
                            :class="getChatClass(chat).main">
                            <q-chip square size="lg">
                                <q-avatar font-size="13px" :color="getChatClass(chat).sub" text-color="white">{{
                                    chat.trade_type }}</q-avatar>
                                <div style="font-size: 12px;">
                                    <div>@{{ chat.trade_price }} </div>
                                    <div class="row">
                                        <div class="col text-container"><span class="truncate">Take profit: {{
                                            chat.take_profit }}</span></div>
                                        <div class="col text-container"><span class="truncate">Trade Status: {{
                                            chat.trade_status }} <q-badge rounded floating color="green" /></span>
                                        </div>
                                    </div>
                                </div>
                            </q-chip>
                        </div>
                    </div>
                </div>
            </transition>
            <q-page-sticky v-show="showScrollTo" position="bottom-right" :offset="fabPos">
                <q-btn round dense color="#1A1A32" icon="arrow_downward" @click="scrollToLastElement('smooth')"
                    :disable="draggingFab" v-touch-pan.prevent.mouse="moveFab">
                    <q-badge v-show="newSignalCount > 0" color="red" floating>{{ newSignalCount }}</q-badge>
                </q-btn>
            </q-page-sticky>
        </q-scroll-area>
        <q-inner-loading :showing="loading" label="Please wait..." label-class="text-teal" label-style="font-size: 1.1em" />
    </div>
</template>

<script>
import {
    mapActions,
    mapState,
} from 'pinia';
import { useQuasar } from 'quasar';

import { useChannelChat } from '../../../lib/store';
import ConversationStart from './conversation_start.vue';

export default {
    name: 'ChannelBodyChat',
    components: {
        ConversationStart
    },
    setup() {
    },
    watch: {
        'currentChannel': {
            handler(channel, before) {
                if (this.ws !== null) {
                    this.leaveChannel()
                }
                this.joinChannel()
                // this.getChannelChatData(channel)
            },
            deep: true
        },
    },
    props: [''],
    computed: {
        ...mapState(useChannelChat, [
            'ws',
            'loading',
            'newSignals',
            'conversations',
            'showChatData',
            'currentChannel',
            'newSignalCount',
            'showScrollTo'
        ]),
        style() {
            let _this = this
            return `height: ${_this.$q.screen.height - 200}px;width: 100%;`
        },
        thumbStyle() {
            return {
                right: '4px',
                borderRadius: '5px',
                backgroundColor: '#027be3',
                width: '5px',
                opacity: 0.75
            }
        },
        barStyle() {
            return {
                right: '2px',
                borderRadius: '9px',
                backgroundColor: '#027be3',
                width: '9px',
                opacity: 0.2
            }
        }
    },
    data() {
        const $q = useQuasar();
        let fabPos = [18, 18];
        let draggingFab = false;
        return {
            $q,
            fabPos,
            draggingFab,
            socket: null,
            requests: 0,
            limit: 1000, // number of requests per minute
            interval: 60000, // interval in milliseconds
            lastElementPosition: null,
            container: undefined,
            subContainer: undefined,
            isNewChannel: true,
        }
    },
    methods: {
        ...mapActions(useChannelChat, [
            'createChannelSocket',
            'loadChannelData',
            'getRefContainer',
            'leaveChannel',
            'joinChannel',
            'handleScroll',
            'setState'
        ]),
        getChatClass(chat) {
            return {
                main: {
                    'you': true,
                    'me': false,
                    'buy': chat.trade_type == 'Buy',
                    'sell': chat.trade_type == 'Sell'
                },
                sub: chat.trade_type == 'Buy' ? 'green' : 'red'
            }
        },
        scrollToLastElement(behavior = 'auto') {
            let _this = this
            this.$nextTick(() => {
                _this.container = _this.$refs.channelChatBody.$el;
                _this.subContainer = _this.container.querySelector('.q-scrollarea__container');
                const lastElement = _this.subContainer.querySelector('.item:last-child');
                if (lastElement) {
                    let lastElePosition = lastElement.offsetTop + lastElement.offsetHeight;
                    _this.lastElementPosition = lastElePosition - _this.subContainer.clientHeight
                    _this.subContainer.scrollBy({
                        top: lastElePosition,
                        behavior: behavior
                    });
                }
            })
        },
        refContainer(callback) {
            this.container = this.$refs.channelChatBody.$el;
            this.subContainer = this.container.querySelector('.q-scrollarea__container');
            const messageRefs = Object.values(this.$refs).filter(ref => ref[0] instanceof HTMLElement && ref[0].classList.contains('new'));
            const isScrollbarAtBottom = this.subContainer.scrollTop >= this.subContainer.scrollHeight - this.subContainer.clientHeight - 28;
            if (messageRefs.length == 0) callback(false, false, isScrollbarAtBottom);
            else messageRefs.forEach(element => callback(element[0], this.subContainer, isScrollbarAtBottom));
        },
        moveFab(ev) {
            this.draggingFab = ev.isFirst !== true && ev.isFinal !== true

            this.fabPos = [
                this.fabPos[0] - ev.delta.x,
                this.fabPos[1] - ev.delta.y
            ]
        },
        dateToHuman(datetimeString) {
            const datetime = new Date(datetimeString);
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
            return datetime.toLocaleString('en-US', options);
        }
    },
    created() {
        if (this.currentChannel) {
            this.createChannelSocket()
        }
    },
    mounted() {
        if (this.currentChannel) {
            this.getRefContainer(this.refContainer)
            this.loadChannelData(this.scrollToLastElement)
        }
    }
}
</script>
<style lang="scss">
:root {
    --white: #fff;
    --black: #000;
    --bg: #f8f8f8;
    --grey: #999;
    --dark: #1a1a1a;
    --light: #e6e6e6;
    --wrapper: 1000px;
    --blue: #00b0ff;
}

.channel-chat-body {
    padding: 10px;
    // overflow-y: auto;

    .text-container {
        width: 132px;
        overflow: hidden;

        .truncate {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
        }
    }

    .conversation-start {
        position: relative;
        width: 100%;
        display: flex;
        margin-bottom: 27px;
        text-align: center;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;

        span {
            display: inline-flex;
            color: var(--light);
            align-items: center;
            font-size: 10px;

            &:before,
            &:after {
                position: absolute;
                display: inline-block;
                width: 30%;
                height: 1px;
                content: '';
                background-color: var(--grey);
            }

            &:before {
                left: 0;
            }

            &:after {
                right: 0;
            }
        }
    }

    .bubble {
        transition-timing-function: cubic-bezier(.4, -.04, 1, 1);

        @for $i from 1 through 10 {
            &:nth-of-type(#{$i}) {
                animation-duration: .15s * $i;
            }
        }
    }

    .bubble {
        font-size: 16px;
        position: relative;
        display: inline-block;
        clear: both;
        margin-bottom: 8px;
        // padding: 13px 14px;
        vertical-align: top;
        border-radius: 5px;

        &:before {
            position: absolute;
            top: 19px;
            display: block;
            width: 8px;
            height: 6px;
            content: '\00a0';
            transform: rotate(29deg) skew(-35deg);
        }

        &.you {
            float: left;
            color: var(--white);
            // background-color: var(--blue);
            align-self: flex-start;
            animation-name: slideFromLeft;

            &.buy {
                &:before {
                    left: 0px;
                    background-color: #4caf50;
                }
            }

            &.sell {
                &:before {
                    left: 0px;
                    background-color: #f44336;
                }
            }
        }

        &.me {
            float: right;
            color: var(--dark);
            background-color: #eceff1;
            padding: 13px 14px;
            align-self: flex-end;
            animation-name: slideFromRight;

            &:before {
                right: -3px;
                background-color: #eceff1;
            }
        }
    }
}

@keyframes slideFromLeft {
    0% {
        margin-left: -200px;
        opacity: 0;
    }

    100% {
        margin-left: 0;
        opacity: 1;
    }
}

@-webkit-keyframes slideFromLeft {
    0% {
        margin-left: -200px;
        opacity: 0;
    }

    100% {
        margin-left: 0;
        opacity: 1;
    }
}

@keyframes slideFromRight {
    0% {
        margin-right: -200px;
        opacity: 0;
    }

    100% {
        margin-right: 0;
        opacity: 1;
    }
}

@-webkit-keyframes slideFromRight {
    0% {
        margin-right: -200px;
        opacity: 0;
    }

    100% {
        margin-right: 0;
        opacity: 1;
    }
}
</style>
