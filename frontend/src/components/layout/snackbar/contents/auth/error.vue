<template>
    <div>
        <div class="text-head">Authentication Error</div>
        <div class="row full">
            <div class="col">
                <div class="text-grey">Unauthorized User</div>
            </div>
            <div class="col">
                <q-btn flat color="white" text-color="black" label="authenticate" @click="openAuthModal" />
                <!-- <div class="text-grey snackbar-action">  </div> -->
            </div>
        </div>
    </div>
</template>

<script>
import { useMainAppStore } from '../../../../../lib/store';

export default {
    name: 'errorSnackBar',
    components: {
    },
    props: [],
    data() {
        const mainApp = useMainAppStore();
        return { mainApp }
    },
    methods: {
        openAuthModal() {
            this.mainApp.setApp('authModal', true)
        }
    }
}
</script>
<style lang="scss">
.full {
    width: 100%;

    .snackbar-action {
        float: right;
    }
}
</style>
