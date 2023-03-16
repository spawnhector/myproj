<template>
    <q-dialog v-model="dialog" :position="position">
        <q-card style="width: 350px">
            <q-card-section class="items-center no-wrap">
                <component :is="childComponent" />
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<script>
import { ref } from 'vue';

import { useMainAppStore } from '../../../lib/store';

export default {
    name: 'snackbar',
    components: {
    },
    props: [],
    data() {
        let MainApp = useMainAppStore();
        const dialog = MainApp.snackbar.active;
        const position = 'bottom';
        let childComponent = MainApp.snackbar.component
        return { dialog, position, MainApp, childComponent }
    },
    created() {
        let _this = this
        this.$watch('MainApp.snackbar', (snackbar) => {
            _this.dialog = snackbar.active
            _this.childComponent = snackbar.component
        })
    },
    methods: {
    }
}
</script>
<style lang="scss">
.text-head {
    color: black;
    font-size: 18px;
}
</style>
