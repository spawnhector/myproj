<template>
    <div class="row wrap justify-center items-center content-center height-fill">
        <div class="col-3 col-sm-6 height-fill">
            <form class="registration_form">
                <div class="form-group">
                    <h5>Create a free account</h5>
                    <q-carousel v-model="slide" animated ref="registration" @transition="updateRegistrationComponent">
                        <q-carousel-slide name="register">
                            <formInput type="text" placeholder="Username" :model="username" icon="badge"
                                field="username" :validate="validateUsername" required="true" :activeform="activeForm"
                                :requesterror="requestError" @value-added="updateUsername" :form="formType" />
                            <formInput type="text" placeholder="Full Name" :model="full_name" icon="person"
                                field="full_name" :validate="validateFullName" required="true" :activeform="activeForm"
                                :requesterror="requestError" @value-added="updateFullName" :form="formType" />
                            <formInput type="email" placeholder="Email" :model="email" icon="email" field="email"
                                :validate="validateEmail" required="true" :activeform="activeForm"
                                :requesterror="requestError" @value-added="updateEmail" :form="formType" />
                            <formInput type="password" placeholder="Password" :model="password" icon="password"
                                field="password" :validate="validatePassword" required="true" :activeform="activeForm"
                                :requesterror="requestError" @value-added="updatePassword" :form="formType" />
                            <div class="submit-cont">
                                <button :disabled="!canContinue" type="button" class="submit"
                                    @click="registrationContinue()">Continue</button>
                            </div>
                        </q-carousel-slide>
                        <q-carousel-slide name="confirmpassword">
                            <formInput type="password" placeholder="Confirm Your Password" :model="confirm_password"
                                icon="password" field="confirm_password" required="true" :activeform="activeForm"
                                :validate="validateConfirmPassword" @value-added="updateConfirmPassword"
                                :requesterror="requestError" :confirm="password" :form="formType" />
                            <div class="submit-cont">
                                <div class="submit-sub-cont">
                                    <button type="button" class="submit" @click="backToRegistration">Back</button>
                                    <appSpacer width="30px" />
                                    <button :disabled="!canRegister" type="button" class="submit"
                                        @click="register">Complete Registration</button>
                                </div>
                            </div>
                        </q-carousel-slide>
                    </q-carousel>
                </div>
            </form>
        </div>
        <!-- <q-separator vertical color="#00000066" /> -->
        <div class="col-3 col-sm-6 height-fill bg-dark-card">
            <h4>Oauth here</h4>
        </div>
    </div>
</template>

<script>
import {
  useAuthStore,
  useMainAppStore,
} from '../../../lib/store.js';
import { UserRegister } from '../../../utils/apiRequest';
import formInput from '../../input/input.vue';
import appSpacer from '../../spacer/spacer.vue';
import InputToolTip from '../../tooltip/inputTooltip.vue';
import validations from './validation.js';

export default {
    name: 'SignUp',
    components: {
        appSpacer, InputToolTip, formInput
    },
    props: ['activeform'],
    data() {
        return {
            auth: useAuthStore(),
            mainApp: useMainAppStore(),
            username: '',
            full_name: '',
            email: '',
            password: '',
            confirm_password: '',
            slide: 'register',
            attemptSubmit: false,
            stage: 1,
            canContinue: false,
            canRegister: false,
            requestError: null,
            errorCount: 0,
            activeForm: null,
            formType: 'registration_form'
        }
    },
    created() {
        let _this = this
        this.$watch('username', (newVal) => {
            _this.formOneValid();
        })
        this.$watch('full_name', (newVal) => {
            _this.formOneValid();
        })
        this.$watch('email', (newVal) => {
            _this.formOneValid();
        })
        this.$watch('password', (newVal) => {
            _this.formOneValid();
        })
        this.$watch('confirm_password', (newVal) => {
            _this.formTwoValid();
        })
        this.$watch('activeform', (newVal) => {
            _this.activeForm = newVal;
        })
        this.$watch('auth.error', (newVal) => {
            console.log(newVal)
            _this.requestError = newVal;
        })
    },
    computed: {
    },
    methods: {
        ...validations,
        updateUsername(val) {
            this.username = val;
        },
        updateFullName(val) {
            this.full_name = val;
        },
        updateEmail(val) {
            this.email = val;
        },
        updatePassword(val) {
            this.password = val;
        },
        updateConfirmPassword(val) {
            this.confirm_password = val;
        },
        registrationContinue() {
            if (this.validateForm()) this.$refs.registration.next();
        },
        backToRegistration() {
            this.auth.setAuth('authLoader', false);
            this.$refs.registration.previous()
        },
        updateRegistrationComponent(newVal, oldVal) {
            this.fixInput()
        },
        fixInput() {
            $(".input").focusin(function () {
                $(this).find("span").animate({ "opacity": "0" }, 200);
            });
            $(".input").focusout(function () {
                $(this).find("span").animate({ "opacity": "1" }, 300);
            });
            $(".registration_form").submit(function () {
                $("input").css({ "border-color": "#2ecc71" });
                return false;
            });
            $("div").removeClass("scroll");
        },
        formOneValid: function () {
            if (this.username != '' && this.full_name != '' && this.email != '' && this.password != '') {
                this.canContinue = true;
            } else {
                this.canContinue = false;
                this.stage = 1;
            }
        },
        formTwoValid: function () {
            if (this.confirm_password === this.password) {
                this.canRegister = true;
            } else {
                this.canRegister = false;
            }
        },
        validateForm: function () {
            if (this.stage === 1 && this.canContinue) {
                this.stage = 2;
                this.auth.setAuth('authLoader', true);
                return true;
            }
            if (this.stage === 2 && this.canRegister) {
                return true;
            }
        },
        register: function () {
            let _this = this;
            if (this.validateForm()) {
                var formData = new FormData();
                formData.append("username", this.username);
                formData.append("full_name", this.full_name);
                formData.append("email", this.email);
                formData.append("password", this.password);
                UserRegister(formData).then(res => {
                    _this.auth.setToken(res.data.token)
                    _this.auth.getToken().then(res => {
                        _this.auth.setAuth('authLoader', false);
                        _this.mainApp.setApp('authModal', false)
                    })
                }, err => {
                    _this.backToRegistration()
                    const keys = Object.keys(err);
                    for (const key of keys) {
                        _this.auth.setAuth('error', `${key}/-/${_this.errorCount}/*/${err[key][0]}`);
                        _this.errorCount++;
                    }
                })
            }
        }
    },
    mounted() {
        this.fixInput()
    }
}
</script>
<style>

</style>
