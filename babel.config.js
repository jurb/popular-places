module.exports = {
  presets: [
    [
      "@vue/app",
      {
        targets: {
          browsers: ["> 1%", "ie 11", "not op_mini all"]
        }
      }
    ]
  ]
};
