<template>
  <q-layout view="hHh lpR fFf">
    <AppLayout />
    <div :style="style" :class="classes.blur">
      <q-page-container :class="classes.step">
        <router-view />
      </q-page-container>
    </div>
    <Blur blurtype="primary" />
  </q-layout>
</template>

<script>
import Blur from './components/layout/blur/blur.vue';
import AppLayout from './components/layout/template.vue';
import {
  useAuthStore,
  useChannelChat,
  useMainAppStore,
} from './lib/store.js';

export default {
  name: 'LayoutDefault',
  components: {
    AppLayout, Blur
  },
  computed: {
    style() {
      return this.channelChat.tutorial.currentStepIndex == 2 ? {
        zIndex: '10001',
        position: 'relative'
      } : {}
    },
    classes() {
      let _this = this;
      return {
        blur: { 'blurred': _this.channelChat.tutorial.currentStepIndex == 2 },
        step: {
          'step-one': _this.channelChat.tutorial.currentStepIndex == 0,
          'step-two': _this.channelChat.tutorial.currentStepIndex == 1,
          'step-three': _this.channelChat.tutorial.currentStepIndex == 2
        }
      }
    },
  },
  data() {
    const channelChat = useChannelChat()
    return {
      MainApp: useMainAppStore(),
      channelChat,
      // AlertMessage: useAlertMessageStore(),
      // AlertNotification: useAlertNotificationStore(),
      modalShow: false,
      main_loading: true,
      setting: false,
      // fixedSetting: '',
      auth: useAuthStore()
    }
  },
  beforeMount() {
    this.auth.getToken()
    // this.checkAuth()
    // console.log(this.auth.isAuthenticatedd)
  },
  created() {
    let _this = this
    this.$watch('MainApp.mobile', (authVal) => {
      _this.setting = _this.mobileSetting(authVal, _this.fixedSetting);
    })
    this.$watch('MainApp.refetch', () => {
      this.getSetting()
    })
    this.$watch('auth.access_token', (newVal) => {
      console.log(newVal)
    })

  },
  methods: {
    // showModal() {
    //   this.modalShow = !this.modalShow;
    // },
    // closeModal() {
    //   this.modalShow = false
    // },
    // mobileSetting(mobile, setting) {
    //   if (setting) if (mobile) return {
    //     ...setting,
    //     moreTabItems: [
    //       ...setting.moreTabItems,
    //       ...setting.tabItems.filter(val => {
    //         return val != setting.tabItems[0]
    //       })
    //     ],
    //     tabItems: [setting.tabItems[0]],
    //   };
    //   return setting;
    // },
    checkAuth() {
      // this.MainApp.is_mobile;
      let _this = this
      console.log('checking auth')
      _this.auth.checkAuth()
    }
  },
  mounted() {
  }
}
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
<style lang="scss">
.blurred {
  animation: fadeIn 5s;
  -webkit-animation: fadeIn 5s;
  -moz-animation: fadeIn 5s;
  -o-animation: fadeIn 5s;
  -ms-animation: fadeIn 5s;

  .step-three {
    .instruction-container {
      position: relative;
      animation: fadeInInstruction 5s;
      -webkit-animation: fadeInInstruction 5s;
      -moz-animation: fadeInInstruction 5s;
      -o-animation: fadeInInstruction 5s;
      -ms-animation: fadeInInstruction 5s;

      .instruction {
        z-index: 1;
        color: #000;
        position: relative;
        display: flex;
        flex-direction: column;
        padding: 25px;
        justify-content: center;
        align-items: center;
        align-content: center;
        flex-wrap: wrap;

        button {
          position: relative;
          top: 10px;
          margin-bottom: 10px;
        }

        .sub-head {
          font-size: 22px;
        }
      }

      .back-drop {
        opacity: 0.6;
        background: white;
        width: -webkit-fill-available;
        height: -webkit-fill-available;
        position: absolute;
        top: 0;
        box-shadow: 0 1px 8px rgb(0 0 0 / 20%), 0 3px 4px rgb(0 0 0 / 14%), 0 3px 3px -2px rgb(0 0 0 / 12%);
      }
    }

    .channel-list {
      &.add-blur {
        opacity: 0.2;
        filter: blur(15px);
      }

      &.add-blur:after {
        opacity: 1;
        filter: blur(0px);
      }

      &.add-free-channel {
        animation: fadeIn 5s;
        -webkit-animation: fadeIn 5s;
        -moz-animation: fadeIn 5s;
        -o-animation: fadeIn 5s;
        -ms-animation: fadeIn 5s;
      }
    }
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0.2;
  }

  100% {
    opacity: 1;
  }
}

@keyframes fadeInInstruction {
  0% {
    filter: blur(15px);
  }

  100% {
    filter: blur(0px);
  }
}
</style>
