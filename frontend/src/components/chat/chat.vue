<template>
    <div class="position-relative" :style="style">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
            <q-layout v-show="showSimulatedReturnData" view="lHh Lpr lFf" class="shadow-3" container>
                <q-header elevated>
                    <q-toolbar class="bg-grey-3 text-black">
                        <q-btn round flat>
                            <q-avatar>
                                <img :src="currentConversation.avatar">
                            </q-avatar>
                        </q-btn>
                        <span class="q-subtitle-1 q-pl-md"
                            v-text="`${auth.isAuthenticated ? '@' + auth.user.username + ' - ' + currentConversation.channel : 'Guest'}`">
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
                            <q-item class="left_drawer_container_items" v-for="(conversation, index) in conversations"
                                :key="conversation.id" clickable v-ripple @click="setCurrentConversation(index)">
                                <q-chip size="30px">
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
  useMainAppStore,
} from '../../lib/store.js';

const conversations = [
    {
        id: 1,
        channel: 'GBPUSD',
        person: 'Razvan Stoenescu',
        avatar: 'https://cdn.quasar.dev/team/razvan_stoenescu.jpeg',
        caption: 'I\'m working on Quasar!',
        time: '15:00',
        sent: true
    },
    {
        id: 2,
        channel: 'USDJPY',
        person: 'Dan Popescu',
        avatar: 'https://cdn.quasar.dev/team/dan_popescu.jpg',
        caption: 'I\'m working on Quasar!',
        time: '16:00',
        sent: true
    },
    {
        id: 3,
        channel: 'GBPUSD',
        person: 'Jeff Galbraith',
        avatar: 'https://cdn.quasar.dev/team/jeff_galbraith.jpg',
        caption: 'I\'m working on Quasar!',
        time: '18:00',
        sent: true
    },
    {
        id: 4,
        channel: 'GBPUSD',
        person: 'Allan Gaunt',
        avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
        caption: 'I\'m working on Quasar!',
        time: '17:00',
        sent: true
    }
]
export default {
    name: 'ChatLayout',
    data: () => {
        const visible = false
        const showSimulatedReturnData = false
        const $q = useQuasar()
        const auth = useAuthStore()
        let leftDrawerOpen = auth.isAuthenticated
        return {
            $q,
            auth,
            visible,
            showSimulatedReturnData,
            leftDrawerOpen,
            search: '',
            message: '',
            currentConversationIndex: 0,
            conversations: conversations,
            socket: null
        }
    },
    computed: {
        currentConversation() {
            return this.conversations[this.currentConversationIndex]
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
            _this.leftDrawerOpen = val
        })
    },
    methods: {
        setCurrentConversation(index) {
            this.currentConversationIndex = index
        },
        getChatData() {
            this.visible = true
            this.showSimulatedReturnData = false
            this.auth.getToken().then(res => {
                this.visible = false
                this.showSimulatedReturnData = true
                this.getChatChannels()
            }, err => {
                this.visible = false
                this.showSimulatedReturnData = true
            })
        },
        getChatChannels() {
            let _this = this;
            _this.socket = new WebSocket('ws://localhost:8000/ws/channel/all/');
            _this.socket.onopen = function (event) {
                _this.socket.send(`ping`);
            };
            _this.socket.onmessage = function (event) {
                let data = JSON.parse(event.data)
                console.log(data)
                // _this.visible = false;
            };
            _this.socket.onclose = function (event) {
                console.log('socket closed')
            };
            _this.socket.onerror = function (error) {
                console.error(`WebSocket error: ${error}`);
            };
        },
    },
    mounted() {
        this.getChatData()
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
.conversation__summary
  margin-top: 4px
.conversation__more
  margin-top: 0!important
  font-size: 1.4rem

.q-item
    padding: 0px !important

.left_drawer_container_items
    left: -2px
</style>
