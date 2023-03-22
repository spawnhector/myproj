<template>
    <span>
        <div>
            <q-chip size="sm" v-show="newSignal" square color="deep-orange" text-color="white"> New Signal </q-chip>
        </div> {{ dateToHuman(mainKey) }}
    </span>
</template>

<script>
export default {
    name: 'ConversationStart',
    components: {
    },
    props: ['mainKey'],
    data() {
        let newSignal = false;
        let newSignalTime = 60;
        return {
            newSignalTime, newSignal
        }
    },
    methods: {

        isNewSignal() {
            let _this = this
            const options = { timeZone: 'America/Jamaica' };
            const givenTime = new Date(new Date(this.mainKey).toLocaleString('en-US', options));
            const currentTime = new Date(new Date().toLocaleString('en-US', options));

            const diffInMilliseconds = currentTime - givenTime;
            const diffInSeconds = diffInMilliseconds / 1000;
            if (diffInSeconds < this.newSignalTime) {
                setTimeout(function () {
                    _this.newSignal = false;
                }, this.newSignalTime * 1000);
                this.newSignal = true;
            } else {
                this.newSignal = false;
            }
        },
        dateToHuman(datetimeString) {
            const datetime = new Date(datetimeString);
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
            return datetime.toLocaleString('en-US', options);
        }
    },
    mounted() {
        this.isNewSignal()
    }
}
</script>
<style></style>
