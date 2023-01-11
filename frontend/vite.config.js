import { defineConfig } from 'vite';

import {
  quasar,
  transformAssetUrls,
} from '@quasar/vite-plugin';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    // <-- this object is added
    port: 80,
  },
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    quasar({
      sassVariables: "src/quasar-variables.sass",
    }),
  ],
});
