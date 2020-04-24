This frontend uses the places API created at https://gitlab.com/commondatafactory/covid19_handhaving/.

To use this frontend with your own places API, please adjust the `d3.json` call in mounted in `/views/Home.vue`.

The api uses basic auth, set the user and pass in these variables in your `.env` and/or `env.local` file

* `VUE_APP_PLACES_API_USER`
* `VUE_APP_PLACES_API_PASS`

The frontend also uses Firebase auth for authentication (no database is used). Adjust the Firebase implementation with your own account credentials by modifying `main.js` and `firebaseConfig.js`, or use your own auth solution.


## Project setup

```
yarn install
```

### Compiles and hot-reloads for development

```
yarn run serve
```

### Compiles and minifies for production

```
yarn run build
```

### Lints and fixes files

```
yarn run lint
```
