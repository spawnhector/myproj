<template>
    <div>
        <q-scroll-area :thumb-style="thumbStyle" :bar-style="barStyle" :style="style">
            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <div v-show="showChatData" class="channel-chat-body" id="channel-chat-body">
                    <span v-for="(chats, mainKey) in conversations" :key="`${chats[0][0]}-conversation-start-${mainKey}`"
                        class="item">
                        <div class="conversation-start">
                            <span>
                                <div>
                                    <q-chip size="sm" square color="deep-orange" text-color="white"> New Signal </q-chip>
                                </div> {{ mainKey }}
                            </span>
                        </div>
                        <div v-for="(chat, subKey) in chats" :key="`${chat[0]}-chat-${subKey}`" class="bubble"
                            :class="getChatClass(chat).main">
                            <q-chip square size="lg">
                                <q-avatar font-size="13px" :color="getChatClass(chat).sub" text-color="white">{{ chat[1]
                                }}</q-avatar>
                                <div style="font-size: 12px;">
                                    <div>@{{ chat[2] }} </div>
                                    <div class="row">
                                        <div class="col text-container"><span class="truncate">Take profit: {{ chat[3]
                                        }}</span></div>
                                        <div class="col text-container"><span class="truncate">Trade Status: {{ chat[5] }}
                                                <q-badge rounded floating color="green" /></span>
                                        </div>
                                    </div>
                                </div>
                            </q-chip>
                        </div>
                    </span>
                </div>
            </transition>
        </q-scroll-area>
        <q-inner-loading :showing="loading" label="Please wait..." label-class="text-teal" label-style="font-size: 1.1em" />
    </div>
</template>

<script>
import { useQuasar } from 'quasar';

export default {
    name: 'ChannelBodyChat',
    components: {
    },
    watch: {
        'currentChannel': {
            handler(channel, before) {
                console.log('here sir', channel)
                this.getChannelChatData(channel)
            },
            deep: true
        }
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
        return {
            $q,
            loading: false,
            showChatData: false,
            socket: null,
            requests: 0,
            limit: 1000, // number of requests per minute
            interval: 60000, // interval in milliseconds
            conversations: {}
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
            this.socket.send(``);
            this.requests++;
        },
        groupByIndex(list) {
            const result = {};
            for (const item of list) {
                const key = item[4];
                if (!result[key]) {
                    result[key] = [];
                }
                result[key].push(item);
            }
            return result;
        },
        createWebSocket(currency) {
            let _this = this;
            this.socket = new WebSocket(`ws://localhost:8000/ws/signals/${currency}/`);
            this.socket.onopen = function (event) {
                _this.socketAction();
            };
            this.socket.onmessage = function (event) {
                let data = JSON.parse(event.data)
                _this.conversations = _this.groupByIndex(data.message)
                _this.loading = false
                _this.showChatData = true
            };
            this.socket.onclose = function (event) {
            };
            this.socket.onerror = function (error) {
                console.error(`WebSocket error: ${error}`);
            };
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
                    'buy': chat[1] == 'Buy',
                    'sell': chat[1] == 'Sell'
                },
                sub: chat[1] == 'Buy' ? 'green' : 'red'
            }
        }
    },
    mounted() {
        this.getChannelChatData(this.currentChannel)
        this.$nextTick(() => {
            const container = document.getElementById('channel-chat-body');
            const lastElement = container.querySelector('.item:last-child');
            console.log(container)
            // container.scrollTop = lastElement.offsetTop - container.offsetHeight + lastElement.offsetHeight;
        })
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
