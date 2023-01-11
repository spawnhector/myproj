<template>
    <div class="custom_input">
        <div class="input">
            <input :id="inputID" :type="type" :placeholder="placeholder" v-model="val" />
            <span><q-icon :name="icon" /></span>
            <q-tooltip v-if="required" transition-show="flip-right" transition-hide="flip-left" :target="targetEl"
                :class="{ 'bg-red': val != '' }" v-model="error[field].state" anchor="center left"
                self="center right">{{ error[field].text }}</q-tooltip>
        </div>
    </div>
</template>

<script>
import InputToolTip from '../tooltip/inputTooltip.vue';

export default {
    name: 'formInput',
    components: {
        InputToolTip
    },
    props: [
        'type',
        'placeholder',
        'model',
        'icon',
        'field',
        'validate',
        'required',
        'confirm',
        'requesterror',
        'showtooltip',
        'form',
        'activeform'
    ],
    data() {
        let val = this.model;
        let field = this.field;
        let form = this.form;
        let targetEl = val == '' ? true : false;
        let inputID = `${form}-${field}-input`;
        return {
            val,
            error: {
                [field]: {
                    state: false,
                    text: 'This field is required'
                },
            },
            targetEl,
            inputID,
            inputElement: false,
            hideFormToolTip: false,
            formType: null
        }
    },
    created() {
        let _this = this
        this.$watch('val', (newVal) => {
            if (newVal == '') {
                _this.$emit(`valueAdded`, '')
                _this.error[_this.field].text = 'This field is required';
                _this.inputElement.style.borderColor = '#ff7052';
                _this.inputElement.addEventListener("blur", function () {
                    this.style.borderColor = 'transparent';
                });
            } else {
                if (_this.validate) {
                    let result = '';
                    if (_this.field == 'confirm_password') {
                        result = _this.validate(newVal, _this.confirm);
                    } else {
                        result = _this.validate(newVal);
                    }
                    if (result.state) {
                        _this.$emit(`valueAdded`, '')
                        _this.inputElement.style.borderColor = '#ff7052';
                    }
                    if (!result.state) {
                        _this.inputElement.style.borderColor = '#646cff';
                        _this.$emit(`valueAdded`, newVal)
                    }
                    _this.targetEl = result.targetEl;
                    _this.error[_this.field].state = result.state;
                    _this.error[_this.field].text = result.text;
                    _this.inputElement.addEventListener("blur", function () {
                        if (result.state) this.style.borderColor = '#ff7052';
                        else this.style.borderColor = 'transparent';
                    });
                }
            }
        })
        this.$watch('requesterror', (err) => {
            let getMessage = err.split('/*/');
            let getType = getMessage[0].split('/-/');
            console.log(getType[0])
            console.log(_this.field)
            if (getType[0] == _this.field) {
                _this.targetEl = true;
                _this.error[_this.field].state = true;
                _this.error[_this.field].text = getMessage[1];
            }
            // if (
            //     getType[0] == 'username' ||
            //     getType[0] == 'full_name' ||
            //     getType[0] == 'email' ||
            //     getType[0] == 'password' &&
            //     _this.form == 'registration_form'
            // ) {
            //     _this.$refs.registration.previous();
            // }
        })
        this.$watch('activeform', (newval) => {
            if (newval != _this.form) {
                _this.targetEl = false;
                _this.error[_this.field].state = false;
            }
        })
    },
    mounted() {
        let _this = this;
        this.$nextTick(() => {
            _this.inputElement = document.getElementById(_this.inputID);
            _this.inputElement.addEventListener("focus", function () {
                if (_this.error[_this.field].state) this.style.borderColor = '#ff7052';
                else this.style.borderColor = '#646cff';
            });
            _this.inputElement.addEventListener("blur", function () {
                this.style.borderColor = 'transparent';
            });
        })
    }
}
</script>
