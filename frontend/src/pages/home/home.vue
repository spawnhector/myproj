<template>
    <q-page padding style="padding-top: 66px">
        <div>
            <q-layout view="lHh Lpr lFf" container style="height: 450px"
                class="shadow-2 rounded-borders sub_layer_container">
                <div style="padding: 20px;padding-top:65px;">
                    <p v-for=" n in 15" :key="n"> Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil
                        praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates
                        asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate? </p>
                </div>
                <q-page-sticky expand position="top">
                    <q-toolbar class="bg-nav text-white">
                        <q-toolbar-title> Page Title </q-toolbar-title>
                    </q-toolbar>
                </q-page-sticky>
            </q-layout>
        </div>
    </q-page>
</template>

<script>

export default {
    name: 'Home',
    components: {
    },
    data: () => ({
    }),
}
</script>
<style lang="sass">
.sub_layer_container
    background: #1A1A2A
</style>
