/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    colors: {
      accent: "#088586",
      "light-grey": "#333333",
    },
    extend: {
      colors: {
        ...colors,
      },
    },
  },
  plugins: [],
};
