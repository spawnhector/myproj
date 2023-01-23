<template>
    <q-item>
        <div v-if="lock" class="channel_disabled_wrapper" @mouseover="showSubscribe()" @mouseleave="hideSubscribe()">
            <div class="channel_disabled_content">
                <q-item-section v-if="show_subscribe" class="subscribe" side>
                    <q-btn flat rounded @click="unlockChannel" label="Unlock" />
                </q-item-section>
                <div class="lock">
                    <q-icon v-if="!unlocking" name="lock" />
                    <q-spinner-rings v-if="unlocking" color="primary" size="2em" />
                </div>
            </div>
            <q-chip size="30px">
                <q-skeleton v-if="skeleton" type="QAvatar" class="chat_list_skeleton_avatar" />
                <q-avatar v-if="!skeleton" color="red" text-color="white"><span style="font-size:13px">{{
                    conversation.channel
                }}</span></q-avatar>
                <q-item-section>
                    <q-skeleton v-if="skeleton" type="rect" class="chat_list_skeleton_item_label_top" />
                    <q-item-label v-if="!skeleton" style="font-size:13px;" lines="1"> {{ conversation.person }}
                    </q-item-label>
                    <q-item-label class="conversation__summary" caption>
                        <q-icon name="check" v-if="conversation.sent" />
                        <q-skeleton v-if="skeleton" type="rect" class="chat_list_skeleton_item_label_bottom" />
                        <q-icon name="not_interested" v-if="conversation.deleted && !skeleton" /> {{
                            conversation.caption
                        }} </q-item-label>
                </q-item-section>
            </q-chip>
        </div>
        <q-chip v-if="!lock" size="30px" :class="{ active_left_drawer_container_items: link === conversation.id }"
            @click="setCurrentConversation">
            <q-skeleton v-if="skeleton" type="QAvatar" class="chat_list_skeleton_avatar" />
            <q-avatar v-if="!skeleton" color="red" text-color="white"><span style="font-size:13px">{{
                conversation.channel
            }}</span></q-avatar>
            <q-item-section>
                <q-skeleton v-if="skeleton" type="rect" class="chat_list_skeleton_item_label_top" />
                <q-item-label v-if="!skeleton" style="font-size:13px;" lines="1"> {{ conversation.person }}
                </q-item-label>
                <q-item-label class="conversation__summary" caption>
                    <q-icon name="check" v-if="conversation.sent" />
                    <q-skeleton v-if="skeleton" type="rect" class="chat_list_skeleton_item_label_bottom" />
                    <q-icon name="not_interested" v-if="conversation.deleted && !skeleton" /> {{ conversation.caption }}
                </q-item-label>
            </q-item-section>
        </q-chip>
    </q-item>
</template>

<script>
import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from '../../../lib/store.js';
import { SubscribeChannels } from '../../../utils/apiRequest';

export default {
    name: 'ChannelItems',
    components: {
    },
    props: ["index", "conversation", "link", "skeleton", "type"],
    data() {
        const channelChat = useChannelChat()
        const mainApp = useMainAppStore()
        const auth = useAuthStore()
        return {
            auth,
            channelChat,
            mainApp,
            show_subscribe: false,
            lock: true,
            unlocking: false
        }
    },
    methods: {
        showSubscribe() {
            this.show_subscribe = true
        },
        hideSubscribe() {
            this.show_subscribe = false
        },
        setCurrentConversation() {
            this.channelChat.setState('link', this.link)
            this.channelChat.setState('currentConversationType', this.type)
            this.channelChat.setState('currentConversationIndex', this.index)
        },
        unlockChannel() {
            let _this = this
            this.unlocking = true
            this.mainApp.setApp('mainLoader', true)
            this.auth.getToken().then(token => {
                let data = new FormData()
                data.append('channel', _this.conversation.id)
                data.append('channel_type', 'Paid')

                SubscribeChannels(token, data).then(res => {
                    console.log(res)
                }, err => {
                    console.log(err)
                })
            })
        },
        // getChatChannels() {
        //     let _this = this;
        //     _this.socket = new WebSocket('ws://localhost:8000/ws/channel/all/');
        //     _this.socket.onopen = function (event) {
        //         _this.socket.send(``);
        //     };
        //     _this.socket.onmessage = function (event) {
        //         let data = JSON.parse(event.data)

        //         _this.link = 20
        //         _this.channels = data.length > 0 ? true : false;
        //         _this.freeChannels.push({
        //             id: 20,
        //             channel: "AUDUSD",
        //             person: 'Allan Gaunt',
        //             avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
        //             caption: 'I\'m working on Quasar!',
        //             time: '17:00',
        //             sent: true
        //         })
        //         data.map(val => {
        //             // console.log(val)
        //             let channel_id = val[0];
        //             let channel_data = val[1];
        //             _this.paidChannels.push({
        //                 id: channel_id,
        //                 channel: channel_data.channel_name,
        //                 person: 'Allan Gaunt',
        //                 avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
        //                 caption: 'I\'m working on Quasar!',
        //                 time: '17:00',
        //                 sent: true
        //             })
        //         })
        //         _this.skeleton = false;
        //         console.log(_this.paidChannels)

        //         // _this.visible = false;
        //     };
        //     _this.socket.onclose = function (event) {
        //         console.log('socket closed')
        //     };
        //     _this.socket.onerror = function (error) {
        //         console.error(`WebSocket error: ${error}`);
        //     };
        // },
    }
}
</script>
<style lang="sass">
.channel_disabled_wrapper
    position: relative
    width: -webkit-fill-available
    .channel_disabled_content
        position: absolute
        z-index: 1
        background-color: #000000b0
        width: -webkit-fill-available
        height: -webkit-fill-available
        .subscribe
            float: right
            top: 6px
            position: relative
            color: #fff
        .lock
            right: 0
            bottom: 0
            position: absolute
    .active_left_drawer_container_items
        background-color: #1A1A32
        color: #d7d7d7
        .q-chip__content
            .q-avatar
                border: 1px solid #fff
        .q-item__label--caption
            color: #d7d7d7 !important
    .chat_list_skeleton_avatar
        width: 60px
        height: 60px
        border-radius: 17px
    .chat_list_skeleton_item_label_top
        height: 20px
    .chat_list_skeleton_item_label_bottom
        height: 16px
    .conversation__summary
        margin-top: 4px

</style>
