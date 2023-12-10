/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    colors: {
      accent: "#1E453E",
      "light-grey": "#181c1c",
      background: "#101010",
    },
    extend: {
      colors: {
        ...colors,
      },
    },
    fontFamily: {
      body: ["Roboto"],
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    // ...
  ],
};
