# E-Porra

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 12.1.2.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Para ejecutar las pruebas end-to-end se debe abrir el proyecto en Cypress que se encuentra en la carpeta `pruebas_e2e` y seguir los siguientes pasos:
1. Instalar dependencias con el comando `npm install`
2. Ejecutar las pruebas con el comando `cypress run --headless`

**Nota:** las pruebas constan de 2 archivos que contienen pruebas basadas en roles, uno para usuario administrador (`adminTests.cy.js`) y otro para usuario apostador  (`apostadorTests.cy.js`) que se encuentran en la carpeta `pruebas_e2e/cypress/e2e/1-getting-started`

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.
