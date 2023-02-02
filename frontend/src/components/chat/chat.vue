<template>
    <div class="position-relative " :style="style.chatMain">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
            <q-layout v-if="(channels_received) && (freeChannels.length > 0 || paidChannels.length > 0)"
                v-show="showSimulatedReturnData" view="lHh Lpr lFf" class="shadow-3 chat-container" container>
                <channelChatHeader :currentChannel="currentChannel" />
                <div :style="style.chatDrawer">
                    <q-drawer style="background: rgba(255, 255, 255, 0.07) !important" v-model="leftDrawerOpen" bordered
                        :breakpoint="690">
                        <q-toolbar class="">
                        </q-toolbar>
                        <q-scroll-area style="height: calc(100% - 100px)">
                            <q-list style="width: 300px" class="channel-list" :class="classes.dsFreeChannel">
                                <span v-if="(freeChannels.length > 0)">
                                    <q-item-label header>Free Channel</q-item-label>
                                    <q-item class="left_drawer_container_items" v-for="(channel, index) in freeChannels"
                                        :key="channel.id" clickable v-ripple>
                                        <channelItems :index="index" :channel="channel" :link="link"
                                            :skeleton="skeleton" type="Free" />
                                    </q-item>
                                </span>
                                <span v-if="(paidChannels.length > 0)">
                                    <q-item-label header>Paid Channels</q-item-label>
                                    <q-intersection class="left_drawer_container_items"
                                        v-for="(channel, index) in paidChannels" :key="channel.id" clickable v-ripple
                                        transition="flip-right">
                                        <channelItems :index="index" :channel="channel" :link="link"
                                            :skeleton="skeleton" type="Paid" />
                                    </q-intersection>
                                </span>
                            </q-list>
                        </q-scroll-area>
                    </q-drawer>
                </div>
                <Blur blurtype="secondary" />
                <q-page-container :style="style.pageContainer">
                    <channelBody :currentChannel="currentChannel" />
                </q-page-container>
                <q-footer style="height: 46px;">
                    <q-toolbar class="row">
                        <q-btn round flat icon="insert_emoticon" class="q-mr-sm" />
                        <q-input rounded outlined dense class="WAL__field col-grow q-mr-sm" bg-color="white"
                            v-model="message" placeholder="Type a message" />
                        <q-btn round flat icon="mic" />
                    </q-toolbar>
                </q-footer>
            </q-layout>
        </transition>
        <q-inner-loading :showing="visible" label="Please wait..." label-class="text-teal"
            label-style="font-size: 1.1em" />
    </div>
</template>

<script>
import { useQuasar } from 'quasar';

import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../lib/store.js';
import { GetChannels } from '../../utils/apiRequest';
import Blur from '../layout/blur/blur.vue';
import channelBody from './channel/channel_body.vue';
import channelItems from './channel/channel_items.vue';
import channelChatHeader from './channel/channelChatHeader.vue';

export default {
    name: 'ChatLayout',
    data: () => {
        const visible = false
        const showSimulatedReturnData = false
        const $q = useQuasar()
        const auth = useAuthStore()
        const channelChat = useChannelChat()
        let leftDrawerOpen = auth.isAuthenticated
        return {
            $q,
            auth,
            channelChat,
            visible,
            showSimulatedReturnData,
            leftDrawerOpen,
            search: '',
            message: '',
            currentChannelIndex: channelChat.currentChannelIndex,
            currentChannelType: channelChat.currentChannelType,
            socket: null,
            channels_received: false,
            freeChannels: [],
            paidChannels: [],
            link: channelChat.link,
            skeleton: true
        }
    },
    components: {
        channelItems,
        channelBody,
        channelChatHeader,
        Blur
    },
    computed: {
        currentChannel() {
            if (this.channelChat.hasSubscribedChannels) {
                if (this.currentChannelType == 'Free') {
                    return this.freeChannels[this.currentChannelIndex]
                } else {
                    return this.paidChannels[this.currentChannelIndex]
                }
            } else {
                return false;
            }
        },
        style() {
            let _this = this
            return {
                chatMain: {
                    height: (_this.$q.screen.height - 57) + 'px',
                    padding: '8px',
                },
                chatDrawer: {
                    zIndex: _this.channelChat.tutorial.dsFreeChannel ? '100000' : 0,
                    position: _this.channelChat.tutorial.dsFreeChannel ? 'absolute' : 'initial',
                },
                pageContainer: {
                    paddingTop: '0px !important',
                    position: 'relative',
                    top: '-7px',
                    paddingBottom: '0px !important',
                    zIndex: _this.channelChat.tutorial.currentStepIndex == 2 ? '10000' : '0'
                },
                currencyList: {
                    zIndex: _this.channelChat.tutorial.currentStepIndex == 2 ? '10000' : '0'
                }
            }
        },
        classes() {
            let _this = this;
            return {
                dsFreeChannel: {
                    'add-free-channel': _this.channelChat.tutorial.dsFreeChannel,
                    'add-blur': !_this.channelChat.tutorial.dsFreeChannel
                }
            }
        },
        isAuth() {
            this.auth.getToken()
        }
    },
    beforeMount() {
    },
    created() {
        let _this = this;
        this.$watch('auth.isAuthenticated', (val) => {
            this.getChatData()
            _this.leftDrawerOpen = val
        })
        this.$watch('channelChat.link', (val) => {
            _this.link = val
        })
        this.$watch('channelChat.currentChannelIndex', (val) => {
            _this.currentChannelIndex = val
        })
        this.$watch('channelChat.currentChannelType', (val) => {
            _this.currentChannelType = val
        })
    },
    watch: {
        'channelChat.channels': {
            handler(channel, before) {
                let _this = this
                let freeChan = []
                let paidChan = []
                let hasFreeChannel = false;
                channel.map((chan, chanIndex) => {
                    if (chan.subscribers.length > 0) {
                        chan.subscribers.map((sub, subindex) => {
                            if (sub.user && sub.user == _this.auth.user.id) {
                                _this.channelChat.setState('hasSubscribedChannels', true)
                                if (!_this.channelChat.initialChannelIndex) {
                                    _this.channelChat.setState('link', chan.id)
                                    _this.channelChat.setState('currentChannelIndex', chanIndex);
                                    _this.channelChat.setState('initialChannelIndex', true);
                                }
                                if (sub.channel_type == 'Paid') {
                                    paidChan.push(_this.addPaidChannel(chan, true))
                                } else {
                                    hasFreeChannel = true;
                                    freeChan.push(_this.addFreeChannel(chan, true))
                                }
                            } else {
                                paidChan.push(_this.addPaidChannel(chan, false))
                            }
                        })
                    } else {
                        paidChan.push(_this.addPaidChannel(chan, false))
                    }
                })
                this.freeChannels = freeChan
                this.paidChannels = paidChan

                if (hasFreeChannel) _this.channelChat.setState('hasFreeChannel', true);
                if (!hasFreeChannel) _this.channelChat.setState('tutorial', {
                    ..._this.channelChat.tutorial,
                    active: true
                });
                if ((_this.freeChannels.length > 0) && (_this.paidChannels.length > 0)) {
                    _this.channelChat.setState('currentChannelType', 'Free')
                } else {
                    _this.channelChat.setState('currentChannelType', 'Paid')
                }
                _this.channels_received = channel.length > 0 ? true : false;
            },
            deep: true
        }
    },
    methods: {
        getChatData() {
            let _this = this;
            this.visible = true
            this.showSimulatedReturnData = false
            this.auth.getToken().then(token => {
                GetChannels(token).then(res => {
                    let data = res.data.channels
                    let arrBuild = []
                    // _this.link = 20
                    data.map(val => {
                        // console.log(val)
                        let channel_data = val;
                        let channel_id = channel_data.id;
                        arrBuild.push({
                            id: channel_id,
                            channel: channel_data.channel_name,
                            subscribers: channel_data.subscribers,
                            person: 'Allan Gaunt',
                            avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
                            caption: 'I\'m working on Quasar!',
                            time: '17:00',
                            sent: true
                        })
                    })
                    _this.channelChat.setState('channels', arrBuild)
                    _this.skeleton = false;
                    this.visible = false
                    this.showSimulatedReturnData = true
                }, err => {
                    console.log(err)
                })
            }, err => {
                this.visible = false
                this.showSimulatedReturnData = true
            })
        },
        addPaidChannel(chan, unlocked) {
            let channel_data = chan;
            let channel_id = channel_data.id;
            return {
                id: channel_id,
                channel: channel_data.channel,
                subscribers: channel_data.subscribers,
                unlocked: unlocked,
                person: 'Allan Gaunt',
                avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
                caption: 'I\'m working on Quasar!',
                time: '17:00',
                sent: true
            }
        },
        addFreeChannel(chan, unlocked) {
            let channel_data = chan;
            let channel_id = channel_data.id;
            return {
                id: channel_id,
                channel: channel_data.channel,
                subscribers: channel_data.subscribers,
                unlocked: unlocked,
                person: 'Allan Gaunt',
                avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
                caption: 'I\'m working on Quasar!',
                time: '17:00',
                sent: true
            }
        }
    },
    mounted() {
    }
}
</script>

<style lang="sass">
.WAL
  width: 100%
  height: 100%
  padding-top: 20px
  padding-bottom: 20px
  &:before
    content: ''
    height: 127px
    position: fixed
    top: 0
    width: 100%
    background-color: #009688
  &__layout
    margin: 0 auto
    z-index: 4000
    height: 100%
    width: 90%
    max-width: 950px
    border-radius: 5px
  &__field.q-field--outlined .q-field__control:before
    border: none
  .q-drawer--standard
    .WAL__drawer-close
      display: none
@media (max-width: 850px)
  .WAL
    padding: 0
    &__layout
      width: 100%
      border-radius: 0
@media (min-width: 691px)
  .WAL
    &__drawer-open
      display: none
.q-item
    padding: 1px 0px !important
.left_drawer_container_items
    left: -1px
    width: -webkit-fill-available
    .q-item
        width: -webkit-fill-available
.q-chip
    width: -webkit-fill-available
.chat-container
    border-radius: 15px
    .q-drawer
        background: #fff0
    .q-field--dense
        .q-field__control
            height: 32px
            color: white
            background-color: rgba(255, 255, 255, 0.19) !important
            .q-field__native
                color: white !important

    .q-footer
        .row
            bottom: 2px
    .q-item__label--header
        padding: 17px

</style>
