<template>
  <q-layout view="hHh lpR fFf">
    <AppLayout />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import AppLayout from './components/layout/template.vue';
import {
  useAuthStore,
  useMainAppStore,
} from './lib/store.js';

export default {
  name: 'LayoutDefault',
  components: {
    AppLayout
  },
  data() {
    return {
      MainApp: useMainAppStore(),
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
