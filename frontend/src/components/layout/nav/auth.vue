<template>
    <div class="__app_authguestnav">
        <div class="q-pl-sm q-gutter-sm row items-center no-wrap">
            <q-btn v-if="$q.screen.gt.xs" dense flat round size="sm" icon="notifications" />
            <q-btn v-if="$q.screen.gt.xs" dense flat>
                <div class="row items-center no-wrap">
                    <q-icon name="add" size="20px" />
                    <q-icon name="arrow_drop_down" size="16px" style="margin-left: -2px" />
                </div>
                <q-menu auto-close>
                    <q-list dense style="min-width: 100px">
                        <q-item clickable class="GL__menu-link">
                            <q-item-section>New repository</q-item-section>
                        </q-item>
                        <q-item clickable class="GL__menu-link">
                            <q-item-section>Import repository</q-item-section>
                        </q-item>
                        <q-item clickable class="GL__menu-link">
                            <q-item-section>New gist</q-item-section>
                        </q-item>
                        <q-item clickable class="GL__menu-link">
                            <q-item-section>New organization</q-item-section>
                        </q-item>
                        <q-separator />
                        <q-item-label header>This repository</q-item-label>
                        <q-item clickable class="GL__menu-link">
                            <q-item-section>New issue</q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
            <q-btn dense flat no-wrap>
                <q-avatar rounded size="20px">
                    <img src="https://cdn.quasar.dev/img/avatar3.jpg">
                </q-avatar>
                <q-icon name="arrow_drop_down" size="16px" />
                <profile-menu />
            </q-btn>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '../../../lib/store.js';
import profileMenu from '../../menu/profileMenu.vue';

export default {
    name: 'AuthNav',
    components: {
        profileMenu
    },
    data() {
        const auth = useAuthStore()

        return {
            auth: auth,
        }
    },
    methods: {
        openAuthModal() {

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
