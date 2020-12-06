# App

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 11.0.2.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.


## Styling
Use color="primary"/"accent"/"warn" for material components. For opacity, colors and font-options of use scss variables.
Overall styling of mat-components occurs in styles.scss. Styling of custom components occurs in corresponding .scss file.

### Colors
- primary-color
- primary-contrast-bw: use this for text on primary color background
- secondary-color: use this for accentuation
- secondary-contrast-bw: use this for text on secondary color background

- threshold-neutral: use this for neutral values
- threshold-positive: use this for positive values
- threshold-negative: use this for negative values

### Font options
Default options for headlines, titles and body are given. For detailed styling, use the following font sizes
- font-size-big/line-height-big: use this for sections
- font-size-medium/line-height-medium: use this for subsections
- font-size-normal/line-height-normal: use this for basic text and tooltips
- font-size-small/line-height-small: use this for hints

### Opacities
The following opacity values are available:
- opacity-normal: 0.8
- opacity-strong: 0.4