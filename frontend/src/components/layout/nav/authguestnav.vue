<template>
    <q-header elevated class="text-white bg-nav" height-hint="61.59">
        <q-toolbar class="q-py-sm q-px-md">
            <!-- <q-btn round dense flat :ripple="false" :icon="fabGithub" size="19px" color="white" class="q-mr-sm"
                no-caps /> -->
            <q-select ref="search" dark dense standout use-input hide-selected class="GL__toolbar-select" color="black"
                :stack-label="false" label="Search or jump to..." v-model="text" :options="filteredOptions" @filter="filter"
                style="width: 300px">
                <template v-slot:append>
                    <img src="https://cdn.quasar.dev/img/layout-gallery/img-github-search-key-slash.svg">
                </template>
                <template v-slot:no-option>
                    <q-item>
                        <q-item-section>
                            <div class="text-center">
                                <q-spinner-pie color="grey-5" size="24px" />
                            </div>
                        </q-item-section>
                    </q-item>
                </template>
                <template v-slot:option="scope">
                    <q-item v-bind="scope.itemProps" class="GL__select-GL__menu-link">
                        <q-item-section side>
                            <q-icon name="collections_bookmark" />
                        </q-item-section>
                        <q-item-section>
                            <q-item-label v-html="scope.opt.label" />
                        </q-item-section>
                        <q-item-section side :class="{ 'default-type': !scope.opt.type }">
                            <q-btn outline dense no-caps text-color="blue-grey-5" size="12px" class="bg-grey-1 q-px-sm"> {{
                                scope.opt.type || 'Jump to' }} <q-icon name="subdirectory_arrow_left" size="14px" />
                            </q-btn>
                        </q-item-section>
                    </q-item>
                </template>
            </q-select>
            <!-- <div v-if="$q.screen.gt.sm"
                class="GL__toolbar-link q-ml-xs q-gutter-md text-body2 text-weight-bold row items-center no-wrap">
                <a href="javascript:void(0)" class="text-white"> Pull requests </a>
                <a href="javascript:void(0)" class="text-white"> Issues </a>
                <a href="javascript:void(0)" class="text-white"> Marketplace </a>
                <a href="javascript:void(0)" class="text-white"> Explore </a>
            </div> -->
            <q-space />
            <guestnav v-if="!auth.isAuthenticated" />
            <authnav v-if="auth.isAuthenticated" />
        </q-toolbar>
        <q-linear-progress v-if="mainloader" indeterminate color="cornflowerblue" />
    </q-header>
</template>

<script>
import { ref } from 'vue';

import { fabGithub } from '@quasar/extras/fontawesome-v6';

import {
    useAuthStore,
    useMainAppStore,
} from '../../../lib/store.js';
import authnav from './auth.vue';
import guestnav from './guest.vue';

const stringOptions = [
    'quasarframework/quasar',
    'quasarframework/quasar-awesome'
]
export default {
    name: 'AuthGuestNav',
    components: {
        guestnav,
        authnav
    },
    data() {
        const authdialog = false
        const maximizedToggle = true
        const text = ''
        const options = null
        const filteredOptions = []
        const search = null // $refs.search
        const auth = useAuthStore()
        const mainApp = useMainAppStore()
        return {
            auth: auth,
            mainApp,
            mainloader: auth.authLoader,
            authdialog,
            maximizedToggle,
            fabGithub,
            text,
            options,
            filteredOptions,
            search,
        }
    },
    created() {
        let _this = this
        this.$watch('auth.authLoader', (authVal) => {
            _this.mainloader = authVal
        })
        this.$watch('mainApp.mainLoader', (Val) => {
            _this.mainloader = Val
        })
    },
    methods: {
        filter(val, update) {
            if (this.options === null) {
                // load data
                setTimeout(() => {
                    this.options = stringOptions
                    this.search.filter('')
                }, 2000)
                update()
                return
            }
            if (val === '') {
                update(() => {
                    this.filteredOptions = this.options.map(op => ({ label: op }))
                })
                return
            }
            update(() => {
                this.filteredOptions = [
                    {
                        label: val,
                        type: 'In this repository'
                    },
                    {
                        label: val,
                        type: 'All GitHub'
                    },
                    ...this.options
                        .filter(op => op.toLowerCase().includes(val.toLowerCase()))
                        .map(op => ({ label: op }))
                ]
            })
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
.q-field--standout
    .q-field__control
        border-radius:50px
</style>
