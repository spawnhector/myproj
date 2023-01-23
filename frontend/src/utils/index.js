export function checkIsAuth(token, url) {
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  if (token) myHeaders.append("Authorization", `Token ${token}`);
  var requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) =>
        JSON.parse(result)
          ? resolve(JSON.parse(result))
          : reject("something went wrong")
      )
      .catch((error) => reject(error));
  });
}

export function getFetch(url) {
  var requestOptions = {
    method: "GET",
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) =>
        JSON.parse(result).status == "200"
          ? resolve(JSON.parse(result))
          : reject("something went wrong")
      )
      .catch((error) => reject(error));
  });
}
export function getExteralFetch(url) {
  var requestOptions = {
    method: "GET",
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) => resolve(JSON.parse(result)))
      .catch((error) => reject(error));
  });
}

export function getTokenFetch(token, url) {
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  myHeaders.append("Authorization", `Token ${token}`);
  var requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) =>
        JSON.parse(result).status == "200"
          ? resolve(JSON.parse(result))
          : reject("something went wrong")
      )
      .catch((error) => reject(error));
  });
}

export function postFetch(data, url) {
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: data,
    redirect: "follow",
  };
  let error = {
    message: "",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) => {
        return JSON.parse(result).status == "200"
          ? resolve(JSON.parse(result))
          : reject(JSON.parse(result));
      })
      .catch((error) => reject(error));
  });
}
export function postTokenFetch(token, data, url) {
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  if (token) myHeaders.append("Authorization", `Token ${token}`);
  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: data,
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) => {
        return JSON.parse(result).status == "200"
          ? resolve(JSON.parse(result))
          : reject("something went wrong");
      })
      .catch((error) => reject(error));
  });
}
export function loginFetch(data, url) {
  var myHeaders = new Headers();
  myHeaders.append("Accept", "application/json");
  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: data,
    redirect: "follow",
  };
  return new Promise((resolve, reject) => {
    fetch(`${url}`, requestOptions)
      .then((response) => response.text())
      .then((result) =>
        JSON.parse(result).token
          ? resolve(JSON.parse(result))
          : reject(
              (function () {
                return JSON.parse(result).detail
                  ? {
                      message: JSON.parse(result).password,
                    }
                  : false;
              })() ||
                (function () {
                  return JSON.parse(result).password
                    ? {
                        type: "Password",
                        message: JSON.parse(result).password,
                      }
                    : false;
                })() ||
                (function () {
                  return JSON.parse(result).username
                    ? {
                        type: "Username",
                        message: JSON.parse(result).username,
                      }
                    : false;
                })() ||
                (function () {
                  return JSON.parse(result).non_field_errors
                    ? {
                        message: JSON.parse(result).non_field_errors,
                      }
                    : false;
                })()
            )
      )
      .catch((error) =>
        reject({
          message: "Please try again later",
        })
      );
  });
}
