<template>
    <div>
        <navHeader />
        <q-drawer v-model="drawerLeft" :width="150" :breakpoint="700" behavior="desktop" bordered class="bg-grey-3">
            <q-scroll-area class="fit">
                <div>
                    <leftDrawerContent />
                </div>
            </q-scroll-area>
        </q-drawer>
        <q-drawer side="right" v-model="drawerRight" bordered :width="150" :breakpoint="500" behavior="desktop"
            class="bg-grey-3">
            <q-scroll-area class="fit">
                <div class="">
                    <rightDrawerContent />
                </div>
            </q-scroll-area>
        </q-drawer>
    </div>
</template>

<script>
import { ref } from 'vue';

import { useQuasar } from 'quasar';

import { useAuthStore } from '../../lib/store';
import leftDrawerContent from './left_drawer/left_drawer_content.vue';
import navHeader from './nav/authGuestNav.vue';
import rightDrawerContent from './right_drawer/right_drawer_content.vue';

export default {
    components: {
        leftDrawerContent,
        rightDrawerContent,
        navHeader
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
