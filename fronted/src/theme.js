import { extendTheme } from "@mui/joy/styles";

const globalTheme = extendTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 250,
      md: 500,
      lg: 750,
      xl: 1000,
    },
  }
});

export default globalTheme;
