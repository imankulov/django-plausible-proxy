# History

## 0.4.0 (2023-03-30)

- Added support for Python 3.11.
- Set timeout for upstream requests and added PLAUSIBLE_REQUEST_TIMEOUT settings option to override it. Thanks @yoshson for the contribution. PR #5.

## 0.3.0 (2022-06-06)

- Added PLAUSIBLE_SCRIPT_PREFIX to make it possible override default location of the proxy script (`js/script.js` -> `${PLAUSIBLE_SCRIPT_PREFIX}/script.js`). Thanks @aareman for the suggestion. Ref #2.

## 0.2.0 (2022-06-06)

- Added PLAUSIBLE_BASE_URL settings option to make it possible to use the project with self-hosted Plausible installations. The default value is https://plausible.io (use the cloud version.) Thanks @aareman for the contribution. PR #1.
- Made PLAUSIBLE_DOMAIN settings optional. If the value is not set, the domain name is taken from the request.
- Added more tests.

## 0.1.2 (2022-04-25)

- Fixed app config

## 0.1.1 (2022-04-25)

- Fixed project metadata

## 0.1.0 (2022-04-25)

- First release on PyPI.
