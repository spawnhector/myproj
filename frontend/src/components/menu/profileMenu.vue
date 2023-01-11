<template>
    <q-menu auto-close>
        <q-list dense>
            <q-item class="GL__menu-link-signed-in">
                <q-item-section>
                    <div>Signed in as <strong>Mary</strong></div>
                </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable class="GL__menu-link">
                <q-item-section>Your profile</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable class="GL__menu-link">
                <q-item-section>Help</q-item-section>
            </q-item>
            <q-item clickable class="GL__menu-link">
                <q-item-section>Settings</q-item-section>
            </q-item>
            <q-item clickable class="GL__menu-link">
                <q-item-section>Sign out</q-item-section>
            </q-item>
        </q-list>
    </q-menu>
</template>

<script>
export default {
    name: 'blank',
    components: {
    },
    props: [],
    data() {
        return {}
    }
}
</script>
<style lang="sass">
.q-menu
    color: #666666 !important
</style>
