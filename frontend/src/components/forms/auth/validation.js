function validateUsername(val) {
  if (val == "") {
    return {
      targetEl: true,
      state: true,
      text: "This field is required",
    };
  }
  if (val != "") {
    if (val.split("").length <= 5) {
      return {
        targetEl: true,
        state: true,
        text: "The username character length must be greater than 5",
      };
    } else {
      return {
        targetEl: false,
        state: false,
        text: "",
      };
    }
  }
}
function validateFullName(val) {
  if (val == "") {
    return {
      targetEl: true,
      state: true,
      text: "This field is required",
    };
  }
  if (val != "") {
    if (val.split("").length <= 5) {
      return {
        targetEl: true,
        state: true,
        text: "The username character length must be greater than 5",
      };
    } else {
      return {
        targetEl: false,
        state: false,
        text: "",
      };
    }
  }
}
function validateEmail(val) {
  if (val == "") {
    return {
      targetEl: true,
      state: true,
      text: "This field is required",
    };
  }
  if (val != "") {
    if (val.split("").length <= 5) {
      return {
        targetEl: true,
        state: true,
        text: "The username character length must be greater than 5",
      };
    } else {
      return {
        targetEl: false,
        state: false,
        text: "",
      };
    }
  }
}
function validatePassword(val) {
  if (val == "") {
    return {
      targetEl: true,
      state: true,
      text: "This field is required",
    };
  }
  if (val != "") {
    if (val.split("").length <= 5) {
      return {
        targetEl: true,
        state: true,
        text: "The username character length must be greater than 5",
      };
    } else {
      return {
        targetEl: false,
        state: false,
        text: "",
      };
    }
  }
}
function validateConfirmPassword(val, password) {
  if (val == "") {
    return {
      targetEl: true,
      state: true,
      text: "This field is required",
    };
  }
  if (val != "") {
    if (val.split("").length <= 5) {
      return {
        targetEl: true,
        state: true,
        text: "The username character length must be greater than 5",
      };
    }
    if (val != password) {
      return {
        targetEl: true,
        state: true,
        text: "Both password and confirm password should be the same",
      };
    }
    return {
      targetEl: false,
      state: false,
      text: "",
    };
  }
}
let validations = {
  validateUsername,
  validateFullName,
  validateEmail,
  validatePassword,
  validateConfirmPassword,
};
export default validations;
