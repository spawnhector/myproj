<template>
    <div class="channel_body" :style="style">
        <div class="arrow arrow--top">
            <svg xmlns="http://www.w3.org/2000/svg" width="270.11" height="649.9" overflow="visible">
                <g class="item-to bounce-1">
                    <path class="geo-arrow draw-in" d="M135.06 142.564L267.995 275.5 135.06 408.434 2.125 275.499z" />
                </g>
                <circle class="geo-arrow item-to bounce-2" cx="194.65" cy="69.54" r="7.96" />
                <circle class="geo-arrow draw-in" cx="194.65" cy="39.5" r="7.96" />
                <circle class="geo-arrow item-to bounce-3" cx="194.65" cy="9.46" r="7.96" />
                <g class="geo-arrow item-to bounce-2">
                    <path class="st0 draw-in" d="M181.21 619.5l13.27 27 13.27-27zM194.48 644.5v-552" />
                </g>
            </svg>
        </div>
        <div class="arrow arrow--bottom">
            <svg xmlns="http://www.w3.org/2000/svg" width="31.35" height="649.9" overflow="visible">
                <g class="item-to bounce-1">
                    <circle class="geo-arrow item-to bounce-3" cx="15.5" cy="580.36" r="7.96" />
                    <circle class="geo-arrow draw-in" cx="15.5" cy="610.4" r="7.96" />
                    <circle class="geo-arrow item-to bounce-2" cx="15.5" cy="640.44" r="7.96" />
                    <g class="item-to bounce-2">
                        <path class="geo-arrow draw-in" d="M28.94 30.4l-13.26-27-13.27 27zM15.68 5.4v552" />
                    </g>
                </g>
            </svg>
        </div>
        <div class="main">
            <div class="main__text-wrapper">
                <Tutorial v-if="channelChat.tutorial.active" />
                <ChannelBodyChat v-if="!channelChat.tutorial.active" />
            </div>
        </div>
    </div>
</template>

<script>
import { useQuasar } from 'quasar';

import {
    useAuthStore,
    useChannelChat,
    useMainAppStore,
} from '../../../lib/store.js';
import ChannelBodyChat from './channel_body_chat.vue';
import Tutorial from './tutorial/tutorial.vue';

export default {
    name: 'ChannelBody',
    components: {
        Tutorial, ChannelBodyChat
    },
    props: [''],
    computed: {
        style() {
            let _this = this
            return `height: ${_this.$q.screen.height - 171}px;background-color: rgb(255 255 255 / 19%);    overflow: hidden !important;`
        }
    },
    created() {
    },
    data() {
        const $q = useQuasar();
        const channelChat = useChannelChat();
        return { $q, channelChat }
    },
    mounted() {
    }
}
</script>
<style lang="scss">
.channel_body {
    margin-top: 58px;
    position: relative;

    .q-carousel {
        background-color: #fff0;
    }

    @import url("https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;1,500&display=swap");

    $purple: #8a15ff;
    $blue: #3800e7;
    $ltblue: #15e0ff;
    $magenta: #d000c5;

    // This is an example of animations & svgs... I completely understand that the amount of absolute positioning in this file is insane... ;) <3

    body {
        background: linear-gradient($blue, $purple);
        height: 100vh;
        font-size: calc(14px + (26 - 14) * ((100vw - 300px) / (1600 - 300)));
        font-family: "DM Mono", monospace;
        font-weight: 300;
        overflow: hidden;
        color: white;
        text-align: center;
    }

    h1 {
        font-size: 3em;
        margin-bottom: 0.2em;
    }

    h2 {
        font-size: 2em;
    }

    .main {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        // position: absolute;
        justify-content: center;
        align-items: center;

        &:before,
        &:after {
            content: "";
            display: block;
            position: absolute;
            z-index: -3;
        }

        &:before {
            right: 0;
            bottom: -19;
            height: 30em;
            width: 30em;
            border-radius: 30em;
            background: linear-gradient($blue, $purple);
            align-self: flex-end;
            animation: gradient-fade 8s ease-in-out 3s infinite alternate;
        }

        &:after {
            $circle-unit: 10em;
            top: 0;
            left: 30;
            height: $circle-unit;
            width: $circle-unit;
            border-radius: $circle-unit;
            background: linear-gradient($blue, $purple);
            animation: gradient-fade-alt 6s ease-in-out 3s infinite alternate;
        }

        &__text-wrapper {
            // position: relative;
            width: 100%;
            padding: 1em;

            &:before,
            &:after {
                content: "";
                display: block;
                position: absolute;
            }

            &:before {
                $circle-unit: 13em;
                z-index: -1;
                top: -3em;
                right: -3em;
                width: $circle-unit;
                height: $circle-unit;
                opacity: 0.7;
                border-radius: $circle-unit;
                background: linear-gradient($ltblue, $purple);
                animation: rotation 7s linear infinite;
            }

            &:after {
                $circle-unit: 20em;
                z-index: -1;
                bottom: -#{$circle-unit};
                width: $circle-unit;
                height: $circle-unit;
                border-radius: $circle-unit;
                background: linear-gradient($magenta, $purple);
                animation: rotation 7s linear infinite;
            }
        }
    }

    .arrow {
        opacity: 0.5;
        position: absolute;

        &--top {
            top: 0;
            left: -5em;
        }

        &--bottom {
            bottom: 0;
            right: 3em;
        }
    }

    .circle {
        transform: translate(50%, -50%) rotate(0deg);
        transform-origin: center;

        &--ltblue {
            $circle-unit: 20em;
            height: $circle-unit;
            width: $circle-unit;
            border-radius: $circle-unit;
            background: linear-gradient($ltblue, $blue);
        }
    }

    .backdrop {
        position: absolute;
        width: 100vw;
        height: 100vh;
        display: block;
        background-color: pink;
    }

    .dotted-circle {
        position: absolute;
        top: 0;
        right: 0;
        opacity: 0.3;
        animation: rotation 38s linear infinite;
    }

    // animations
    .draw-in {
        stroke-dasharray: 1000;
        stroke-dashoffset: 10;
        animation: draw 15s ease-in-out alternate infinite;
    }

    @keyframes draw {
        from {
            stroke-dashoffset: 1000;
        }

        to {
            stroke-dashoffset: 0;
        }
    }

    .item-to {
        animation-duration: 10s;
        animation-iteration-count: infinite;
        transform-origin: bottom;
    }

    .bounce-1 {
        animation-name: bounce-1;
        animation-timing-function: ease;
    }

    .bounce-2 {
        animation-name: bounce-2;
        animation-timing-function: ease;
    }

    .bounce-3 {
        animation-name: bounce-3;
        animation-timing-function: ease;
    }

    @keyframes bounce-1 {
        0% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(50px);
        }

        100% {
            transform: translateY(0);
        }
    }

    @keyframes bounce-2 {
        0% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-30px);
        }

        100% {
            transform: translateY(0);
        }
    }

    @keyframes bounce-3 {
        0% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(30px);
        }

        100% {
            transform: translateY(0);
        }
    }

    // gradient fade

    @keyframes rotation {
        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }
    }

    @keyframes gradient-fade {
        from {
            transform: translate(10%, -10%) rotate(0deg);
        }

        to {
            transform: translate(50%, -50%) rotate(360deg);
        }
    }

    @keyframes gradient-fade-alt {
        from {
            transform: translate(-20%, 20%) rotate(0deg);
        }

        to {
            transform: translate(-60%, 60%) rotate(360deg);
        }
    }

    .geo-arrow {
        fill: none;
        stroke: #fff;
        stroke-width: 2;
        stroke-miterlimit: 10
    }
}
</style>
