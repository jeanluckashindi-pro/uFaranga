/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Roboto', 'sans-serif'],
        'roboto': ['Roboto', 'sans-serif'],
        'anton': ['Anton', 'sans-serif'],
        'bangers': ['Bangers', 'cursive'],
        'cookie': ['Cookie', 'cursive'],
      },
    },
  },
  plugins: [],
}
