import {
  checkIsAuth,
  getFetch,
  getTokenFetch,
  loginFetch,
  postFetch,
  postTokenFetch,
} from './index.js';

let backend = "http://localhost:8000";
export const CheckAuthToken = (token) =>
  checkIsAuth(token, `${backend}/api/v1/user/`);
export const UserLogin = (data) => loginFetch(data, `${backend}/api/v1/login/`);
export const UserRegister = (data) =>
  postFetch(data, `${backend}/api/v1/register/`);
export const UserLogout = () => getFetch(`${backend}/api/v1/logout/`);
export const GetSignals = () => getFetch(`${backend}/api/v1/signals/`);
export const GetChannels = (token) =>
  getTokenFetch(token, `${backend}/api/v1/channels/`);
export const SubscribeChannels = (token, data) =>
  postTokenFetch(token, data, `${backend}/api/v1/channels_subscribe/`);
