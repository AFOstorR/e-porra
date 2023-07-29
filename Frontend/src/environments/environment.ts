// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
const backendUrl = "http://127.0.0.1:5000";
const eventosUrl = "http://127.0.0.1:5001";
const apuestasUrl = "http://127.0.0.1:5002";
const ingressUrl = "http://35.222.198.0"
export const environment = {
  production: false,
  backendUrl,
  eventosUrl,
  apuestasUrl,
  ingressUrl
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
