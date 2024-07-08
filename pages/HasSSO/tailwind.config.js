/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors')

export default {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: colors.black,
            white: colors.white,
            gray: colors.gray,
            emerald: colors.emerald,
            indigo: colors.indigo,
            yellow: colors.yellow,
            'hana': {
                '600': '#127253',
                '500': '#009086'
            }
        },
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
}
