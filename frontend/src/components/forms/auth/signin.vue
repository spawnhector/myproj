<template>
    <div class="row wrap justify-center items-center content-center height-fill">
        <div class="col-3 col-sm-6 height-fill">
            <form class="login_form">
                <div class="form-group">
                    <h5>Sign in to your account</h5>
                    <formInput type="text" placeholder="Username" :model="username" icon="badge" field="username"
                        :validate="validateUsername" required="true" @value-added="updateUsername"
                        :requesterror="requestError" :activeform="activeForm" :form="formType" />
                    <formInput type="password" placeholder="Password" :model="password" icon="password" field="password"
                        :validate="validatePassword" required="true" @value-added="updatePassword"
                        :requesterror="requestError" :activeform="activeForm" :form="formType" />
                    <p class="forgot-pass">Forgot password?</p>
                    <div class="submit-cont">
                        <button :disabled="!canLogin" type="button" class="submit" @click="login">Sign In</button>
                    </div>
                </div>
            </form>
        </div>
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
import { UserLogin } from '../../../utils/apiRequest';
import formInput from '../../input/input.vue';
import validations from './validation.js';

export default {
    name: 'SignInForm',
    components: {
        formInput
    },
    props: ['activeform'],
    data: () => ({
        auth: useAuthStore(),
        mainApp: useMainAppStore(),
        username: '',
        password: '',
        canLogin: false,
        requestError: '',
        errorCount: 0,
        activeForm: null,
        formType: 'login_form',
    })
    ,
    created() {
        let _this = this
        this.$watch('username', (newVal) => {
            _this.formValid();
        })
        this.$watch('password', (newVal) => {
            _this.formValid();
        })
        this.$watch('activeform', (newVal) => {
            _this.activeForm = newVal;
        })

    },
    mounted() {
        $(".input").focusin(function () {
            $(this).find("span").animate({ "opacity": "0" }, 200);
        });
        $(".input").focusout(function () {
            $(this).find("span").animate({ "opacity": "1" }, 300);
        });
        $(".login").submit(function () {
            $("input").css({ "border-color": "#2ecc71" });
            return false;
        });
    },
    methods: {
        ...validations,
        updateUsername(val) {
            this.username = val;
        },
        updatePassword(val) {
            this.password = val;
        },
        formValid: function () {
            if (this.username != '' && this.password != '') {
                this.canLogin = true;
            } else {
                this.canLogin = false;
            }
        },
        validateForm: function () {
            if (this.canLogin) {
                this.auth.setAuth('authLoader', true);
                return true;
            }
        },
        login: function () {
            let _this = this;
            if (this.validateForm()) {
                var formData = new FormData();
                formData.append("username", this.username);
                formData.append("password", this.password);
                UserLogin(formData).then(res => {
                    _this.auth.setToken(res.token)
                    if (_this.auth.getToken()) {
                        _this.auth.setAuth('authLoader', false);
                        _this.mainApp.setApp('authModal', false)
                    }
                }, err => {
                    _this.requestError = `error-count-${_this.errorCount}/*/${err.message[0]}`;
                    _this.errorCount++;
                    _this.auth.setAuth('authLoader', false);
                })
            }
        }
    }
}
</script>
<style lang="scss">

</style>
