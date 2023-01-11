<template>
    <q-dialog v-model="dialog" persistent :maximized="maximizedToggle" transition-show="slide-up"
        transition-hide="slide-down" @hide="closeModal()">
        <q-card class="bg-dark-container  text-white">
            <q-bar>
                <q-space />
                <q-btn dense flat icon="minimize" @click="maximizedToggle = false" :disable="!maximizedToggle">
                    <q-tooltip v-if="maximizedToggle" class="bg-white text-primary">Minimize</q-tooltip>
                </q-btn>
                <q-btn dense flat icon="crop_square" @click="maximizedToggle = true" :disable="maximizedToggle">
                    <q-tooltip v-if="!maximizedToggle" class="bg-white text-primary">Maximize</q-tooltip>
                </q-btn>
                <q-btn dense flat icon="close" v-close-popup>
                    <q-tooltip class="bg-white text-primary">Close</q-tooltip>
                </q-btn>
            </q-bar>
            <q-card-section class="authModal">
                <q-linear-progress v-if="mainLoader" indeterminate color="cornflowerblue" />
                <div class="cont">
                    <div class="form sign-in row wrap justify-center items-center content-center">
                        <div class="_cont ">
                            <signinform :activeform="activeForm" />
                        </div>
                    </div>
                    <div class="sub-cont">
                        <div class="img">
                            <div class="img__text m--up">
                                <h2>New here?</h2>
                                <p>Sign up and discover great amount of new opportunities!</p>
                            </div>
                            <div class="img__text m--in">
                                <h2>One of us?</h2>
                                <p>If you already has an account, just sign in. We've missed you!</p>
                            </div>
                            <div class="img__btn" @click="togggleSignup()">
                                <span class="m--up">Sign Up</span>
                                <span class="m--in">Sign In</span>
                            </div>
                        </div>
                        <div class="form sign-up full-width row wrap justify-center items-center content-center">
                            <div class="_cont ">
                                <signupform :activeform="activeForm" />
                            </div>
                        </div>
                    </div>
                </div>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<script>
import {
  useAuthStore,
  useMainAppStore,
} from '../../../../lib/store.js';
import signinform from '../../../forms/auth/signin.vue';
import signupform from '../../../forms/auth/signup.vue';

export default {
    name: 'AuthModal',
    components: {
        signinform, signupform
    },
    props: [
        // dialog,
        // maximizedToggle,
    ],
    data() {
        const mainApp = useMainAppStore()
        const auth = useAuthStore()
        return {
            auth,
            dialog: mainApp.authModal,
            maximizedToggle: true,
            mainApp,
            mainLoader: false,
            showToolTip: true,
            activeForm: 'login_form',
            oldForm: 'registration_form'
        }
    },
    created() {
        let _this = this
        this.$watch('mainApp.authModal', (newVal) => {
            _this.dialog = newVal;
        })
        this.$watch('maximizedToggle', (newVal) => {
            console.log('maximizedToggle', newVal)
        })
        this.$watch('auth.authLoader', (newVal) => {
            _this.mainLoader = newVal
        })
    },
    computed: {

    },
    methods: {
        closeModal() {
            this.mainApp.setApp('authModal', false)
        },
        togggleSignup() {
            let storeOldForm = this.activeForm;
            this.activeForm = this.oldForm;
            this.oldForm = storeOldForm;
            this.showToolTip = !this.showToolTip;
            document.querySelector('.cont').classList.toggle('s--signup');
        }
    },
    mounted() {
        // this.$nextTick(() => {
        //     console.log(document.querySelector('.img__btn'))
        //     // document.querySelector('.img__btn').addEventListener('click', function () {
        //     //     document.querySelector('.cont').classList.toggle('s--signup');
        //     // });
        // })
    }
}
</script>
<style lang="scss" scoped>
$contW: 100%;
$imgW: 20%;
$formW: $contW - $imgW;
$switchAT: 1.2s;

$inputW: 260px;
$btnH: 36px;

$diffRatio: (
    $contW - $imgW) / $contW;

@mixin signUpActive {
    .cont.s--signup & {
        @content;
    }
}

.authModal {
    .form {
        position: relative;
        width: $formW;
        height: 100%;
        transition: transform $switchAT ease-in-out;
        // padding: 50px 30px 0;
    }

}


.tip {
    font-size: 20px;
    margin: 40px auto 50px;
    text-align: center;
}

.cont {
    overflow: hidden;
    position: relative;
    width: $contW;
    height: 100vh - 5vh;
    background: #1A1A32;
}

.sub-cont {
    overflow: hidden;
    position: absolute;
    left: $formW;
    top: 0;
    width: $contW;
    height: 100%;
    padding-left: $imgW;
    background: #1A1A32;
    transition: transform $switchAT ease-in-out;

    @include signUpActive {
        transform: translate3d($formW * -1, 0, 0
        );
}
}

.q-bar--standard {
    height: 5vh !important;
}

.q-card__section--vert {
    padding: 0 !important;
}


.img {
    overflow: hidden;
    z-index: 2;
    position: absolute;
    left: 0;
    top: 0;
    width: $imgW;
    height: 100%;
    padding-top: 360px;

    &:before {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        width: $contW * 5;
        height: 100%;
        background-image: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/142996/sections-3.jpg');
        background-size: cover;
        transition: transform $switchAT ease-in-out;
    }

    &:after {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
    }

    @include signUpActive {
        &:before {
            transform: translate3d($formW, 0, 0);
        }
    }

    &__text {
        z-index: 2;
        position: absolute;
        left: 80%;
        top: 50px;
        width: 100%;
        padding: 0 20px;
        text-align: center;
        color: #fff;
        transition: transform $switchAT ease-in-out;

        h2 {
            margin-bottom: 10px;
            font-weight: normal;
        }

        p {
            font-size: 14px;
            line-height: 1.5;
        }

        &.m--up {
            transform: translateX($formW * -1);

            @include signUpActive {
                transform: translateX($formW);
            }
        }

        &.m--in {
            transform: translateX($formW);

            @include signUpActive {
                transform: translateX($formW * -1);
            }
        }
    }

    &__btn {
        overflow: hidden;
        z-index: 2;
        position: relative;
        width: 100px;
        top: $formW - $imgW;
        height: $btnH;
        margin: 0 auto;
        background: transparent;
        color: #fff;
        text-transform: uppercase;
        font-size: 15px;
        cursor: pointer;

        &:after {
            content: '';
            z-index: 2;
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            border: 2px solid cornflowerblue;
            border-radius: 30px;
        }

        span {
            position: absolute;
            left: 0;
            top: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            transition: transform $switchAT;

            &.m--in {
                transform: translateY($btnH*-2);

                @include signUpActive {
                    transform: translateY(0);
                }
            }

            &.m--up {
                @include signUpActive {
                    transform: translateY($btnH*2);
                }
            }
        }
    }
}


.forgot-pass {
    margin-top: 15px;
    text-align: center;
    font-size: 12px;
    color: #cfcfcf;
}

.submit {
    margin-top: 40px;
    margin-bottom: 20px;
    background: #d4af7a;
    text-transform: uppercase;
}

.fb-btn {
    border: 2px solid #d3dae9;
    color: darken(#d3dae9, 20%);

    span {
        font-weight: bold;
        color: darken(#768cb6, 20%);
    }
}

.sign-in {
    transition-timing-function: ease-out;

    @include signUpActive {
        transition-timing-function: ease-in-out;
        transition-duration: $switchAT;
        transform: translate3d($formW, 0, 0);
    }

}

.sign-up {
    transform: translate3d($contW * -1, 0, 0);

    @include signUpActive {
        transform: translate3d(0, 0, 0);
    }

}

._cont {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 6px;
    width: 80%;
    height: $formW;
    border: 1px solid cornflowerblue;
}

.icon-link {
    position: absolute;
    left: 5px;
    bottom: 5px;
    width: 32px;

    img {
        width: 100%;
        vertical-align: top;
    }

    &--twitter {
        left: auto;
        right: 5px;
    }
}
</style>
