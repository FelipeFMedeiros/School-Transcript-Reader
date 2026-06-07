import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import babel from 'vite-plugin-babel';

export default defineConfig({
    plugins: [
        tailwindcss(),
        babel({
            include: [/\.[jt]sx?$/],
            exclude: [/node_modules/],
            babelConfig: {
                presets: ['@babel/preset-typescript'],
                plugins: [['babel-plugin-react-compiler', { target: '19' }]],
            },
        }),
        react(),
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
});
