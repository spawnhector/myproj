<template>
    <div class="__app_authguestnav">
        <q-btn round dense flat :ripple="true" icon="login" size="19px" color="white" class="q-mr-sm"
            @click="openAuthModal()" no-caps />
        <AuthModal />
    </div>
</template>

<script>
import {
  useAuthStore,
  useMainAppStore,
} from '../../../lib/store.js';
import AuthModal from '../modal/auth/auth.vue';

export default {
    name: 'GuestNav',
    components: {
        AuthModal,
    },
    data() {
        const auth = useAuthStore()
        const mainApp = useMainAppStore()
        return {
            auth,
            mainApp
        }
    },
    methods: {
        openAuthModal() {
            this.mainApp.setApp('authModal', true)
        }
    }
}
</script>
<style lang="sass">
.__app_authguestnav
    float: right
    margin-left: 10px
    .q-icon
        font-size: 26px
        cursor: pointer
</style>
