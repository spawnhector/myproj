<template>
    <div class="position-relative" :style="style">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
            <q-layout v-if="(channels_received) && (freeChannels.length > 0 || paidChannels.length > 0)"
                v-show="showSimulatedReturnData" view="lHh Lpr lFf" class="shadow-3" container>
                <q-header elevated>
                    <q-toolbar class="bg-grey-3 text-black">
                        <q-btn round flat>
                            <q-avatar>
                                <img :src="currentChannel.avatar">
                            </q-avatar>
                        </q-btn>
                        <span class="q-subtitle-1 q-pl-md"
                            v-text="`${auth.isAuthenticated ? '@' + auth.user.username + ' - ' + currentChannel.channel : 'Guest'}`">
                        </span>
                        <q-space />
                        <q-btn round flat icon="search" />
                        <q-btn round flat>
                            <q-icon name="attachment" class="rotate-135" />
                        </q-btn>
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
                <q-drawer v-model="leftDrawerOpen" bordered :breakpoint="690">
                    <q-toolbar class="bg-grey-2">
                        <q-input rounded outlined dense class="WAL__field full-width" bg-color="white" v-model="search"
                            placeholder="Search or start a new conversation">
                            <template v-slot:prepend>
                                <q-icon name="search" />
                            </template>
                        </q-input>
                    </q-toolbar>
                    <q-scroll-area style="height: calc(100% - 100px)">
                        <q-list style="width: 300px">
                            <span v-if="(freeChannels.length > 0)">
                                <q-item-label header>Free Channel</q-item-label>
                                <q-item class="left_drawer_container_items" v-for="(conversation) in freeChannels"
                                    :key="conversation.id" clickable v-ripple>
                                    <q-chip size="30px"
                                        :class="{ active_left_drawer_container_items: link === conversation.id }">
                                        <q-avatar color="red" text-color="white"><span style="font-size:13px">{{
                                            conversation.channel
                                        }}</span></q-avatar>
                                        <q-item-section>
                                            <q-item-label style="font-size:13px;" lines="1"> {{ conversation.person }}
                                            </q-item-label>
                                            <q-item-label class="conversation__summary" caption>
                                                <q-icon name="check" v-if="conversation.sent" />
                                                <q-icon name="not_interested" v-if="conversation.deleted" /> {{
                                                    conversation.caption
                                                }} </q-item-label>
                                        </q-item-section>
                                        <q-item-section side>
                                            <q-item-label caption> {{ conversation.time }} </q-item-label>
                                            <q-icon name="keyboard_arrow_down" />
                                        </q-item-section>
                                    </q-chip>
                                </q-item>
                            </span>
                            <span v-if="(paidChannels.length > 0)">
                                <q-item-label header>Paid Channels</q-item-label>
                                <q-intersection class="left_drawer_container_items"
                                    v-for="(channel, index) in paidChannels" :key="channel.id" clickable v-ripple
                                    transition="flip-right">
                                    <channelItems :index="index" :channel="channel" :link="link" :skeleton="skeleton"
                                        type="paid" />
                                </q-intersection>
                            </span>
                        </q-list>
                    </q-scroll-area>
                </q-drawer>
                <q-page-container style="padding-top: 0px !important;" class="bg-grey-2">
                    <!-- <router-view /> -->
                </q-page-container>
                <q-footer>
                    <q-toolbar class="bg-grey-3 text-black row">
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
import channelItems from './channel/channel_items.vue';

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
        channelItems
    },
    computed: {
        currentChannel() {
            if (this.currentChannelType == 'free') {
                return this.freeChannels[this.currentChannelIndex]
            } else {
                return this.paidChannels[this.currentChannelIndex]
            }
        },
        style() {
            let _this = this
            return {
                height: (_this.$q.screen.height - 62) + 'px'
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
            console.log(_this.link)
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
                channel.map(chan => {
                    if (chan.subscribers.length > 0) {
                        chan.subscribers.map(sub => {
                            if (sub.user && sub.user == _this.auth.user.id) {
                                if (sub.channel_type == 'Paid') {
                                    _this.addPaidChannel(chan, true)
                                } else {
                                    _this.addFreeChannel(chan)
                                }
                            } else {
                                _this.addPaidChannel(chan, false)
                            }
                        })
                    } else {
                        _this.addPaidChannel(chan, false)
                    }
                })

                if ((_this.freeChannels.length > 0) && (_this.paidChannels.length > 0)) {
                    _this.channelChat.setState('currentChannelType', 'free')
                } else {
                    _this.channelChat.setState('currentChannelType', 'paid')
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
                    // _this.link = 20
                    data.map(val => {
                        // console.log(val)
                        let channel_data = val;
                        let channel_id = channel_data.id;
                        _this.channelChat.channels.push({
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
            this.paidChannels.push({
                id: channel_id,
                channel: channel_data.channel,
                subscribers: channel_data.subscribers,
                unlocked: unlocked,
                person: 'Allan Gaunt',
                avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
                caption: 'I\'m working on Quasar!',
                time: '17:00',
                sent: true
            })
        },
        addFreeChannel(chan) {
            let channel_data = chan;
            let channel_id = channel_data.id;
            this.freeChannels.push({
                id: channel_id,
                channel: channel_data.channel,
                subscribers: channel_data.subscribers,
                person: 'Allan Gaunt',
                avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
                caption: 'I\'m working on Quasar!',
                time: '17:00',
                sent: true
            })
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
    left: -2px
    width: -webkit-fill-available
.q-chip
    width: -webkit-fill-available

</style>