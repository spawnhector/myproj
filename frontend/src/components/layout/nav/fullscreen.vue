<template>
    <div class="__app_fullscreen">
        <q-icon v-if="toggle === false" name="fullscreen" @click="fullScreen()" />
        <q-icon v-else name="fullscreen_exit" class="cursor-pointer" @click="exitFullScreen()" />
    </div>
</template>

<script>
import { ref } from 'vue'
import { AppFullscreen } from 'quasar'
export default {
    name: 'FullScreen',
    setup() {
        const toggle = ref(false)
        function fullScreen() {
            AppFullscreen.request()
                .then(() => {
                    toggle.value = true
                })
                .catch(err => {
                    // oh, no!!!
                })
        }
        function exitFullScreen() {
            AppFullscreen.exit()
                .then(() => {
                    toggle.value = false
                })
                .catch(err => {
                    // oh, no!!!
                })
        }
        return {
            toggle,
            fullScreen,
            exitFullScreen
        }
    }
}
</script>
<style lang="sass">
.__app_fullscreen
    float: right
    .q-icon
        font-size: 26px
        cursor: pointer
</style>
