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
import { useQuasar } from 'quasar';

import ConversationStart from './conversation_start.vue';

export default {
    name: 'ChannelBodyChat',
    components: {
        ConversationStart
    },
    watch: {
        'currentChannel': {
            handler(channel, before) {
                if (this.socket !== null) {
                    const message = { action: 'leave_group' };
                    this.socket.send(JSON.stringify(message));
                }
                this.getChannelChatData(channel)
            },
            deep: true
        },
    },
    props: ['currentChannel'],
    computed: {
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
        let newSignals = {};
        let newSignalCount = 0;
        return {
            $q,
            fabPos,
            draggingFab,
            newSignals,
            newSignalCount,
            loading: false,
            showChatData: false,
            socket: null,
            requests: 0,
            limit: 1000, // number of requests per minute
            interval: 60000, // interval in milliseconds
            conversations: false,
            lastElementPosition: null,
            showScrollTo: false,
            container: undefined,
            subContainer: undefined,
            isNewChannel: true
        }
    },
    methods: {
        socketAction() {
            if (this.requests >= this.limit) {
                this.socket.close()
                return;
            }
            if (Date.now() - this.lastCheck > this.interval) {
                this.lastCheck = Date.now();
                this.requests = 0;
            }
            const message = { action: 'join_group' };
            this.socket.send(JSON.stringify(message));
            this.requests++;
        },
        groupByIndex(list) {
            const result = {};
            for (const item of list) {
                const key = item.trade_date;
                if (!result[key]) {
                    result[key] = [];
                }
                result[key].push(item);
            }
            return result;
        },
        createWebSocket(currency) {
            let _this = this;
            _this.socket = new WebSocket(`ws://localhost:8000/ws/test_signals/${currency}/client/?token=a02b74b5994a2fd776f19911272266623f87b569049dccee4a96453e606a3909`);

            let timeout = setTimeout(function () {
                if (_this.socket.readyState !== WebSocket.CLOSED) {
                    const message = { action: 'leave_group' };
                    _this.socket.send(JSON.stringify(message));
                    _this.socket.close();
                    _this.socket = null;
                    console.log('WebSocket timed out');
                }
            }, 5000);
            _this.socket.onopen = function (event) {
                _this.socketAction();
            };
            _this.socket.onmessage = function (event) {
                const message = JSON.parse(event.data);
                if (message.action === 'group_joined') {
                    _this.conversations = _this.groupByIndex(message.message.signals)
                    _this.loading = false
                    _this.showChatData = true
                    _this.scrollToLastElement();
                } else if (message.action === 'group_left') {
                    _this.newSignalCount = 0;
                    _this.showScrollTo = false;
                    _this.newSignals = {};
                    _this.isNewChannel = true;
                } else if (message.action === 'new_signal') {
                    _this.checkNewSignal(_this.groupByIndex(message.message.signals))
                }
                clearTimeout(timeout);
            };
            _this.socket.onclose = function (event) {
                console.log('chat channel closed')
                clearTimeout(timeout);
            };
            _this.socket.onerror = function (error) {
                console.log(`WebSocket error: ${JSON.stringify(error)}`);
                clearTimeout(timeout);
            };
        },
        checkNewSignal(newSignal) {
            let _this = this;
            let signalKeys = this.findNewSignals(newSignal, this.conversations);
            if (signalKeys.length == 0) return;
            signalKeys.forEach(signalKey => this.newSignals[signalKey] = true);
            this.newSignalCount = this.countSignal()
            this.conversations = newSignal
            function showScrollTo(messageRect, containerRect, isScrollbarAtBottom) {
                if (isScrollbarAtBottom) {
                    _this.showScrollTo = true;
                }
            }
            this.refContainer(showScrollTo)
        },
        getChannelChatData(data) {
            this.loading = true
            this.showChatData = false
            this.createWebSocket(data.channel)
        },
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
        scrollToLastElement(behavior) {
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
            });
        },
        refContainer(callback) {
            this.container = this.$refs.channelChatBody.$el;
            this.subContainer = this.container.querySelector('.q-scrollarea__container');
            const messageRefs = Object.values(this.$refs).filter(ref => ref[0] instanceof HTMLElement && ref[0].classList.contains('new'));
            const isScrollbarAtBottom = this.subContainer.scrollTop >= this.subContainer.scrollHeight - this.subContainer.clientHeight - 28;
            if (messageRefs.length == 0) callback(false, false, isScrollbarAtBottom);
            else messageRefs.forEach(element => callback(element[0], this.subContainer, isScrollbarAtBottom));
        },
        handleScroll() {
            let _this = this;
            function decrementSignal(messageRect, containerRect, isScrollbarAtBottom) {
                if (isScrollbarAtBottom) {
                    _this.showScrollTo = false;
                } else {
                    _this.showScrollTo = true;
                }
                if (messageRect && containerRect) {
                    const message = messageRect.getBoundingClientRect();
                    const container = containerRect.getBoundingClientRect();
                    if (message.top <= container.bottom) {
                        if (_this.newSignals[messageRect.getAttribute('name')]) _this.newSignals[messageRect.getAttribute('name')] = false;
                        _this.newSignalCount = _this.countSignal()
                    }
                }
            }
            _this.refContainer(decrementSignal)
        },
        moveFab(ev) {
            this.draggingFab = ev.isFirst !== true && ev.isFinal !== true

            this.fabPos = [
                this.fabPos[0] - ev.delta.x,
                this.fabPos[1] - ev.delta.y
            ]
        },
        countSignal() {
            let total = 0;
            Object.entries(this.newSignals).forEach((sig) => {
                if (sig[1]) total += 1
            })
            return total
        },
        findNewSignals(a, b) {
            const signalsKey = [];
            for (const key in a) {
                if (!(key in b)) {
                    signalsKey.push(key);
                }
            }
            return signalsKey;
        },
        dateToHuman(datetimeString) {
            const datetime = new Date(datetimeString);
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
            return datetime.toLocaleString('en-US', options);
        }
    },
    updated() {

    },
    created() {
        this.getChannelChatData(this.currentChannel)

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
