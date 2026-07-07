import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5659,          // 改为其他可用端口
    strictPort: false,   // 若端口被占用则自动尝试下一个
    host: '0.0.0.0'      // 允许局域网访问（可选）
  }
})