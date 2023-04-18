<template>
    <div>
        <q-table class="my-sticky-column-table" card-class="bg-main-sub" bordered :rows="rows" :columns="columns"
            row-key="name" hide-header hide-bottom>
            <template v-slot:body="props">
                <q-tr :props="props">
                    <q-td key="name" :props="props"> {{ props.row.name }} </q-td>
                    <q-td key="data" :props="props">
                        <q-btn size="sm" flat rounded v-if="props.row.name == 'Trade Ticket'" icon="tag" color="primary"
                            href="start/pick-quasar-flavour" target="_blank" :label="props.row.data" />
                        <span v-if="props.row.name == 'Magic Number'">{{ props.row.data }}</span>
                        <span v-if="props.row.name == 'Gains'">{{ props.row.data }}</span>
                    </q-td>
                </q-tr>
            </template>
        </q-table>
    </div>
</template>

<script>
import {
    mapActions,
    mapState,
} from 'pinia';

import {
    useMainAppStore,
    useToolTipStore,
} from '../../lib/store';

export default {
    name: 'SignalOpen',
    components: {
    },

    props: [],
    computed: {
        ...mapState(useToolTipStore, [
            'columns',
            'rows'
        ]),
        ...mapState(useMainAppStore, [
            'constants',
        ]),
    },
    data() {
        return { showTooltip: true }
    },
    methods: {
        reState() {
            // this.showTooltip = true;
        },
        viewTradeTicket() {
            // console.log(row.data)
        }
    },
    mounted() {
        let _this = this
        _this.$nextTick(() => {
        })
    }
}
</script>
<style></style>
