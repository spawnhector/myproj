import './styles/quasar.scss';
import '@quasar/extras/material-icons/material-icons.css';
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css';
import '@quasar/extras/mdi-v4/mdi-v4.css';

import { AppFullscreen } from 'quasar';

// To be used on app.use(Quasar, { ... })
export default {
  config: {},
  plugins: {
    AppFullscreen
  }
}
