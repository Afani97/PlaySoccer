import $$ from 'dom7'
import Framework7 from 'framework7/framework7.esm.bundle.js'

// Import F7 Styles
import 'framework7/css/framework7.bundle.css'

// Import Icons and App Custom Styles
import '../css/icons.css'
import '../css/app.css'
// Import Cordova APIs
import cordovaApp from './cordova-app.js'
// Import Routes
import routes from './routes.js'

const app = new Framework7({ // eslint-disable-line no-unused-vars
  root: '#app', // App root element
  id: 'com.aristotelfani.playsoccer', // App bundle ID
  name: 'PlaySoccer', // App name
  theme: 'auto', // Automatic theme detection
  autoDarkTheme: true,
  // App routes
  routes: routes,
  // Input settings
  input: {
    scrollIntoViewOnFocus: Framework7.device.cordova && !Framework7.device.electron,
    scrollIntoViewCentered: Framework7.device.cordova && !Framework7.device.electron
  },
  // Cordova Statusbar settings
  statusbar: {
    iosOverlaysWebView: true,
    androidOverlaysWebView: false
  },
  on: {
    init: function () {
      var f7 = this

      if (f7.device.cordova) {
        // Init cordova APIs (see cordova-app.js)
        cordovaApp.init(f7)
      }
    }
  }
})
