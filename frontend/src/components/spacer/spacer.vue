<template>
    <span :style="style"></span>
</template>

<script>
export default {
    name: 'appSpacer',
    props: ['width'],
    components: {
    },
    data() {

        let style = {
            width: this.width
        }
        return {
            style
        }
    }
}
</script>
<style>

</style>
