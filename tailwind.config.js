/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./*.html"
  ],
  theme: {
    extend: {
      colors: {
        'allianza': {
          'primary': '#3b82f6',
          'secondary': '#8b5cf6',
          'dark': '#1f2937',
          'darker': '#111827'
        }
      }
    },
  },
  plugins: [],
}

