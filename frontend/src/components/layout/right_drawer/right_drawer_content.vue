<template>
    <q-scroll-area class="fit side-container">
        <div id="vue-list-animation-test" class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-12">
                    <ul class="list-group">
                        <transition-group name="list-complete" tag="li">
                            <li v-for="item in items" v-bind:key="item"
                                class="list-group-item list-complete-item rounded"> item {{ item }}</li>
                        </transition-group>
                    </ul>
                </div>
                <!-- <div class="col-12 text-center my-3">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button @click="add" type="button" class="btn btn-secondary">Add</button>
                    <button @click="shuffle" type="button" class="btn btn-secondary">Shuffle</button>
                    <button @click="remove" type="button" class="btn btn-secondary">Remove</button>
                </div>
            </div> -->
            </div>
        </div>
    </q-scroll-area>
</template>

<script>
export default {
    name: 'RightDrawerContent',
    components: {
    },
    data: () => ({
        items: [1, 2, 3, 4, 5],
        nextNum: 6
    }),
    methods: {
        randomIndex() {
            return Math.floor(Math.random() * this.items.length)
        },
        add() {
            this.items.splice(this.randomIndex(), 0, this.nextNum++)
        },
        remove() {
            this.items.splice(this.randomIndex(), 1)
        },
        arrShuffle(array) {
            let currentIndex = array.length, randomIndex;
            while (currentIndex != 0) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;
                [array[currentIndex], array[randomIndex]] = [
                    array[randomIndex], array[currentIndex]];
            }

            return array;
        },
        shuffle: function () {
            this.items = this.arrShuffle(this.items);
        }
    }
}
</script>
<style>
/* ul.list-group {
    list-style-type: none;
}

.list-complete-item {
    transition: all .6s;
}

.list-complete-enter,
.list-complete-leave-to {
    opacity: 0;
    transform: translateY(35px);
}

.list-complete-leave-active {
    position: relative;
    display: block;
}

.list-group-item.rounded {
    border-radius: 30px !important;
    margin-bottom: 5px;
} */
</style>
