<template>
    <div>
        <navHeader />
        <q-drawer v-model="drawerLeft" :width="250" :breakpoint="700" behavior="desktop" bordered
            class="side-container-wrapper">
            <leftDrawerContent />
        </q-drawer>
        <q-drawer side="right" v-model="drawerRight" bordered :width="250" :breakpoint="500" behavior="desktop"
            class="side-container-wrapper">
            <rightDrawerContent />
        </q-drawer>
    </div>
</template>

<script>
import { ref } from 'vue';

import { useQuasar } from 'quasar';

import { useAuthStore } from '../../lib/store';
import Blur from './blur/blur.vue';
import leftDrawerContent from './left_drawer/left_drawer_content.vue';
import navHeader from './nav/authGuestNav.vue';
import rightDrawerContent from './right_drawer/right_drawer_content.vue';

export default {
    components: {
        leftDrawerContent,
        rightDrawerContent,
        navHeader,
        Blur
    },
    data() {
        const $q = useQuasar();
        const auth = useAuthStore();
        return {
            auth: auth,
            drawerLeft: $q.screen.width > 700,
            drawerRight: $q.screen.width > 500
        }
    }
}
</script>
<style>
.side-container {}

.side-container-wrapper {
    background-color: #24292e;
    padding: 8px;
}
</style>
