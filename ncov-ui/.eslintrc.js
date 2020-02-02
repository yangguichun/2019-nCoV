module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'on' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'on' : 'off'
  },
  parserOptions: {
    parser: 'babel-eslint'
  }
}
